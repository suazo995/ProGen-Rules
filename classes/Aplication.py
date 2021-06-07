import glob
import os
import re
from classes.DBConnect import DBConnect
from pygtrie import StringTrie


class App:
    """
    Clase que modela una app.

    :param path: path de la aplicación.
    """

    def __init__(self, path):
        # se registra el nombre y el path, andemas de los path de los archivos configuradores.
        self.name = path.split('/')[-1]
        self.path = path
        self.buildGradleFiles = self.findFilePaths(path, "*uild.gradle")
        self.propertiesPaths = self.findFilePaths(path, "*roject.properties")
        self.dontObfuscateRule = False
        self.dontObfuscateFiles = []
        self.classes = []
        self.proguardRuleFiles = []
        self.packageLocations = StringTrie(separator='.')
        self.classLoadResourceFromAPK = StringTrie(separator='.')
        self.classLoadedByJNIOnNativeSide = StringTrie(separator='.')

        # se ve si esta activado proguard y donde estan los archivos de reglas
        isObfGradle = self.isAppObfuscatedG(self.buildGradleFiles)
        isObfProp = self.isAppObfuscatedP(self.propertiesPaths)

        # Si se existen archivos de reglas en uso, significa que se usa proguard y tiene reglas
        self.isObf = (len(isObfGradle) != 0) or (len(isObfProp) != 0)

        if self.isObf:
            # si esta ofuscado se buscan las reglas y los nombres de las clases

            javaClassesPaths = self.findFilePaths(path, "*.java")
            ktClassesPaths = self.findFilePaths(path, "*.kt")

            for pth in javaClassesPaths:
                if 'src/main/' in pth:
                    self.classes.append(JavaClass(pth, self))
            for pth in ktClassesPaths:
                if 'src/main/' in pth:
                    self.classes.append(KtClass(pth, self))

            proguardRulePaths = []
            for ruleFileName in (isObfProp + isObfGradle):
                proguardRulePaths.extend(self.findFilePaths(path, ruleFileName))

            for pth in proguardRulePaths:
                file = ProGuard(pth, self)
                self.proguardRuleFiles.append(file)
        # se registran las dependencias
        self.dependencies = self.extractDependencies(self.buildGradleFiles)
        self.detectJavaCodeCalledFromNativeInstances()

    def getRules(self):
        retRules = []
        for pg in self.getPgFiles():
            retRules.extend(pg.getRules())
        retRules = list(set(retRules))
        return retRules

    def getClasses(self):
        return self.classes

    def getPgFiles(self):
        """Entrega los objetos de los archivos de reglas proguard."""
        return self.proguardRuleFiles

    def getNumberOfRules(self):
        totalRules = 0
        for pg in self.proguardRuleFiles:
            totalRules += len(pg.rules.rules)
        return totalRules

    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def getGradlePaths(self):
        """Entrega paths de archivos configuradores gradle"""
        return self.buildGradleFiles

    def getProjectPropertiesPath(self):
        """ Entrega los path de los archivos project.properties"""
        return self.propertiesPaths

    def getDontObfuscateRule(self):
        """ Entrega bool si el app tiene la regla dontObfuscate."""
        return self.dontObfuscateRule

    def getDontObfuscateFiles(self):
        """ Entrega paths de los archivos proguard que tengan la regla dontObfuscate"""
        return self.dontObfuscateFiles

    def getIsObf(self):
        """ Entrega si esta ofuscada o no"""
        return self.isObf

    def getDependencies(self):
        """ Entrega las dependencias del app"""
        return self.dependencies

    def getAllImports(self):
        try:
            imports = []

            for cl in self.getClasses():
                imports.extend(cl.getImports())

            return imports
        except TypeError:
            print(self.getClasses())

    def isObfuscated(self):
        return self.isObf

    def findFilePaths(self, path, file):
        return glob.glob(path + "/**/" + file, recursive=True)

    """ Se ve si estan ofuscadas y donde se encuentran los archivos de reglas"""

    def isAppObfuscatedG(self, build):
        ruleFiles = []
        for file in build:
            obfuscated = False
            proguardFiles = False
            count_bracket = 0

            with open(file) as myFile:

                for line in myFile:
                    ln = line.split("//")[0]

                    if 'proguardFile ' in ln:
                        ruleFiles.extend(re.findall("(?:'|\")(.*?\..*?)(?:'|\")", ln))

                    if 'proguardFiles' in ln:
                        proguardFiles = True

                    if (re.search('minifyEnabled\s*=*\s*[tT(enable)]', ln)
                        or re.search('useProguard\s*=*\s*[tT(enable)]', ln)) \
                            and not re.search('useProguard\s*=*\s*[fF(disable)]', line):
                        obfuscated = True

                    if obfuscated and proguardFiles:
                        if '{' in ln:
                            count_bracket += 1

                        if 'fileTree' in ln:
                            if 'dir' in ln:
                                search = "dir: '(.*?)'"
                            else:
                                search = "'(.*?)'"
                            for direct in re.findall(search, ln):
                                ruleFiles.extend(os.listdir('/'.join(file.split('/')[0:-1]) + "/" + direct))
                        else:
                            ruleFiles.extend(re.findall("'(.*?\..*?)'", ln))
                        if '}' in ln:
                            if count_bracket == 0:
                                break
                            else:
                                count_bracket -= 1
        return ruleFiles

    def isAppObfuscatedP(self, prop):
        ruleFiles = []
        for file in prop:
            try:

                with open(file, 'r') as myFile:
                    for line in myFile:
                        ln = line.split("#")[0].split("!")[0]
                        if 'proguard.config' in ln:
                            ln = ln.split('=')[1].split(":")
                            for l in ln:
                                ruleFilesNames = re.findall('(.*?\.txt)', l.split("\\")[-1])
                                if ruleFilesNames:
                                    for rf in ruleFilesNames:
                                        ruleFiles.append(rf)
            except UnicodeDecodeError:
                print(UnicodeDecodeError, "\nerror en " + file + "\n")
        return ruleFiles

    def extractDependencies(self, build):
        """
        Se entrega lista de dependecias

        :param build: path de archivo gradle.
        :return:
        """
        dependencies = []

        for file in build:
            deps = False
            count_bracket = 0
            with open(file) as myFile:

                for line in myFile:
                    ln = line.split("//")[0]

                    if 'dependencies' in ln:
                        deps = True
                        continue
                    if 'def' in ln:
                        continue
                    if deps:
                        if '{' in ln:
                            count_bracket += 1
                        if 'exclude' in ln and 'module' in ln:
                            continue
                        elif 'fileTree' in ln:
                            if 'dir' in ln:
                                search = "dir: (?:'|\")(.*?)(?:'|\")"
                            else:
                                search = "(?:'|\")(.*?)(?:'|\")"
                            for direct in re.findall(search, ln):
                                try:
                                    for dep in os.listdir('/'.join(file.split('/')[0:-1]) + "/" + direct):
                                        dependencies.append(dep.split(".")[0])
                                except (FileNotFoundError, NotADirectoryError):
                                    pass
                        elif 'files' in ln:
                            dependencies.extend(re.findall("/(.*?)(?:'|\")", ln))
                        elif 'project' in ln:
                            dependencies.extend(re.findall("(?:':|\":)(.*?)(?:'|\")", ln))
                        elif 'Libraries' in ln:
                            dependencies.extend(re.findall("\.([-a-zA-Z0-9_]*)\)?", ln))
                        elif 'name:' in ln and 'group:' in ln:
                            dependencies.extend(re.findall("name: *\t*(?:'|\")(.*?)(?:'|\")", ln))
                        else:
                            dependencies.extend(re.findall(":(.*?):", ln))
                        if '}' in ln:
                            if count_bracket == 0:
                                deps = False
                            else:
                                count_bracket -= 1

        ret = list(dict.fromkeys(dependencies).keys())
        if ret is None:
            return []
        return ret

    def saveInDB(self, db: DBConnect):
        appId = db.saveApp(self)
        db.saveDeps(appId, self.getDependencies())
        db.saveRules(appId, self.getRules())
        db.saveImports(appId, self.getAllImports())

    def rulesForDepInApp(self, dep, prnt=False, f=None):
        """
            Entrega las reglas para una dependencia en específico.

            :param self: Objeto analisador de una app, dep: Nombre de la dependencia.
            :return: lista de reglas atinentes a la dependencia.
        """

        imports = self.getAllImports()
        relatedImports = []

        for im in imports:
            if dep in im:
                imAAgregar = im.split(".")[-1]
                if imAAgregar == "*" or imAAgregar == "**":
                    imAAgregar = im.split(".")[-2]
                if imAAgregar not in relatedImports:
                    relatedImports.append(imAAgregar)

        rulesForThisDep = []
        compRules = []

        for pg in self.getPgFiles():
            lastRuleForDepSeenIndx = -1

            for idx, rule in enumerate(pg.getRules()):
                if dep in rule:
                    if prnt: f.write("-" + rule + "\n")
                    rulesForThisDep.append(rule)

                    lastRuleForDepSeenIndx = idx
                else:
                    if lastRuleForDepSeenIndx != -1 and (idx - lastRuleForDepSeenIndx) <= 3:
                        if prnt: f.write("-" + rule + "\t# por proximidad" + "\n")
                        rulesForThisDep.append(rule)
                    for im in relatedImports:
                        if im in rule:
                            if prnt: f.write("-" + rule + "\t# del import: " + im + "\n")
                            if rule not in rulesForThisDep:
                                rulesForThisDep.append(rule)
                        else:
                            if (rule, dep) not in compRules:
                                compRules.append((rule, dep))

        return [rulesForThisDep, compRules]

    def rulesForDeps(self):
        """
            Entrega las reglas para todas las dependencias de la app.

            :param self: Objeto analisador de una app.
            :return: lista de reglas atinentes a las dependencias de la app.
        """
        rulesForDeps = []

        for dep in self.dependencies:
            rulesForDeps.extend(self.rulesForDepInApp(dep)[0])

        return rulesForDeps

    def appendPgFile(self, fileToInclude):
        pgFile = ProGuard(fileToInclude, self)
        self.proguardRuleFiles.append(pgFile)

    def insertClassPackageLocation(self, packageLocation, className):
        trie = self.packageLocations

        if packageLocation not in trie.keys():
            trie[packageLocation] = [className]
        else:
            temp = trie.pop(packageLocation)
            temp.append(className)
            trie[packageLocation] = temp

        self.packageLocations = trie

    def getPackageLocations(self):
        return self.packageLocations

    def isInPackageStructure(self, classLocationReference):
        separateClassAndElement = classLocationReference.rsplit('.', 1)

        if len(separateClassAndElement) > 1:
            locationReference = separateClassAndElement[0]
            classReference = separateClassAndElement[1]

            packageLocationsTrie = self.getPackageLocations()

            if classReference == '**' and packageLocationsTrie.has_subtrie(locationReference):
                return True

            elif packageLocationsTrie.has_key(locationReference):
                return True
        else:
            return False

    def insertClassLoadedByJNI(self, packageLocation, className):
        trie = self.classLoadedByJNIOnNativeSide

        if packageLocation not in trie.keys():
            trie[packageLocation] = [className]
        else:
            temp = trie.pop(packageLocation)
            temp.append(className)
            trie[packageLocation] = temp

        self.classLoadedByJNIOnNativeSide = trie

    def getClassesLoadedByJNI(self):
        return self.classLoadedByJNIOnNativeSide

    def isInClassesLoadedByJNI(self, classLocationReference):
        separateClassAndElement = classLocationReference.rsplit('.', 1)

        if len(separateClassAndElement) > 1:
            locationReference = separateClassAndElement[0]
            classReference = separateClassAndElement[1]

            classesLoadedByJNITrie = self.getClassesLoadedByJNI()

            if classReference == '**' and classesLoadedByJNITrie.has_subtrie(locationReference):
                return True

            elif classesLoadedByJNITrie.has_key(locationReference):
                return True
        else:
            return False

    def insertClassLoadResourceFromAPK(self, packageLocation, className):
        trie = self.classLoadResourceFromAPK

        if packageLocation not in trie.keys():
            trie[packageLocation] = [className]
        else:
            temp = trie.pop(packageLocation)
            temp.append(className)
            trie[packageLocation] = temp

        self.classLoadResourceFromAPK = trie

    def getClassesLoadingResourceFromAPK(self):
        return self.classLoadResourceFromAPK

    def getRulesForResourceLoadingFromAPK(self):
        APKClasses = self.getClassesLoadingResourceFromAPK()
        return self.getRulesForClasses(APKClasses, "keepnames class ")

    def getRulesForClasses(self, classes, rulePrefix, ruleSuffix=''):

        allClasses = self.getPackageLocations()

        returnRules = []

        for key in classes.keys():
            resourceLoadingClasses = classes[key]
            if key not in allClasses.keys():
                for clss in resourceLoadingClasses:
                    rule = rulePrefix + key + '.' + clss.split('.', 1)[0] + ruleSuffix
                    if rule not in returnRules:
                        returnRules.append(rule)
            else:
                classesInSameLocation = allClasses[key]

                representation = len(resourceLoadingClasses)/len(classesInSameLocation)*100
                if representation >= 50:
                    returnRules.append(rulePrefix + key + ".*" + ruleSuffix)
                else:
                    for clss in resourceLoadingClasses:
                        rule = rulePrefix + key + '.' + clss.split('.', 1)[0] + ruleSuffix
                        if rule not in returnRules:
                            returnRules.append(rule)
        return returnRules

    def detectJavaCodeCalledFromNativeInstances(self):

        returnClasses = []

        for folder, dirs, files in os.walk(self.path):
            for file in files:
                JNIClassCall = False
                JNIEnvDeclaration = False
                includeJNIDeclaration = False

                fullpath = os.path.join(folder, file)
                extension = fullpath.rsplit('.', 1)[-1]

                if extension == "cpp" or extension == "c":
                    try:
                        with open(fullpath, 'r') as f:
                            for line in f:
                                match_class_call = re.findall(".*->FindClass\((.*?)\).*", line)
                                match_JNIenv_declaration = re.findall(".*JNIEnv\*.*", line)
                                match_include_JNI_declaration = re.findall(".*#include (?:<|\")jni.h(?:>|\")", line)
                                if match_class_call:
                                    JNIClassCall = True
                                if match_JNIenv_declaration:
                                    JNIEnvDeclaration = True
                                if match_include_JNI_declaration:
                                    includeJNIDeclaration = True
                                if (JNIClassCall and includeJNIDeclaration) or JNIEnvDeclaration:
                                    break
                        with open(fullpath, 'r') as f:
                            if (JNIClassCall and includeJNIDeclaration) or JNIEnvDeclaration:
                                match = re.findall("\"([a-zA-Z0-9]+?/[a-zA-Z0-9]+?[a-zA-Z0-9/]*?)\"", f.read(), re.MULTILINE)
                                if match:
                                    returnClasses.extend(match)
                    except:
                        print(fullpath.split("obfApps/", 1)[1])
        reformatClasses = list(map(lambda x: x.replace('/', '.'), returnClasses))
        for clss in reformatClasses:
            clssSplit = clss.rsplit('.', 1)
            packageLocation = clssSplit[0]
            className = clssSplit[1]
            self.insertClassLoadedByJNI(packageLocation, className)

    def getRulesForClassesLoadedFromNativeSide(self):
        JNIClasses = self.getClassesLoadedByJNI()
        return self.getRulesForClasses(JNIClasses, "keep, includedescriptorclasses class ", " { *; }")


class Rules:

    def __init__(self, rules):
        self.rules = rules


def isolate_class_specifications(rule):
    class_specification_rules = ['keep', 'keepclassmembers', 'keepclasseswithmembers', 'keepnames',
                                 'keepclassmembernames', 'keepclasseswithmembernames', 'dontwarn', 'dontnote']
    if " extends " in rule or " implements " in rule:
        classAndExtended = rule.split(' extends ')
        if len(classAndExtended) == 1:
            classAndExtended = rule.split(' implements ')
        if '@' in classAndExtended[1]:
            classBeingExtended = classAndExtended[1].split(' ', 2)[1]
        else:
            classBeingExtended = classAndExtended[1].split(' ', 1)[0]
        extendingClass = classAndExtended[0].rsplit(' ', 1)[-1]
        return [extendingClass, classBeingExtended]

    elif rule.split(' ', 1)[0] in class_specification_rules:
        classLocationReference = rule.split(' {', 1)[0].rsplit(' ', 1)

        if len(classLocationReference) < 2:
            return []
        classLocationReference = classLocationReference[1]

        return [classLocationReference]
    return []


class ProGuard:
    """
    Clase que modela un archivo proguard.
    """

    def __init__(self, path, app):
        self.name = path.split('/')[-1]
        self.path = path
        self.defaultFile = (self.name == 'proguard-rules.pro')
        self.rules = Rules(self.findFileRules(path, app))

    def getRules(self):
        return self.rules.rules

    # funcion find Rules
    #
    # recive: path de la aplicacion y objeto aplicacion
    #
    # retorna: reglas de ofuscacion
    def findFileRules(self, path: str, app: App):

        rulesToFilter = ['dontskipnonpubliclibraryclasses', 'skipnonpubliclibraryclasses',
                         'forceprocessing', 'dontshrink', 'printusage', 'whyareyoukeeping', 'dontoptimize',
                         'optimizations', 'optimizationpasses', 'assumenosideeffects', 'assumenoexternalsideeffects',
                         'assumenoescapingparameters', 'assumenoexternalreturnvalues', 'assumevalues',
                         'allowaccessmodification', 'mergeinterfacesaggressively', 'printmapping', 'applymapping',
                         'obfuscationdictionary', 'classobfuscationdictionary', 'packageobfuscationdictionary',
                         'overloadaggressively', 'useuniqueclassmembernames', 'dontusemixedcaseclassnames',
                         'flattenpackagehierarchy', 'repackageclasses', 'dontpreverify', 'microedition', 'verbose',
                         'ignorewarnings', 'printconfiguration', 'dump', 'addconfigurationdebugging']
        try:
            with open(path, 'r') as file:
                ret = []
                opened_rule = re.sub(r'(?m)^\s*#.*\n?', '', file.read())
                opened_rule = ' '.join(opened_rule.split())
                opened_rule = re.split("^-| -", opened_rule)[1:]
                # opened_rule = opened_rule.split("-")[1:]
                pattern = re.compile('[^a-zA-Z0-9_*.,;<>(){}@/!$ -]+')
                if opened_rule:
                    for rule in opened_rule:
                        if "dontobfuscate" in rule:
                            app.dontObfuscateRule = True
                            app.dontObfuscateFiles.append(path)
                        elif "include " in rule:
                            fileToInclude = rule.split()[1]
                            pathToInclude = path.rsplit('/', 1)[0] + '/' + fileToInclude
                            app.appendPgFile(pathToInclude)
                        elif rule.split()[0] not in rulesToFilter:
                            rule = pattern.sub('', rule.replace("\\n", "").replace("\\r", "")).rstrip()

                            if rule == "dontwarn":
                                continue

                            classSpecification = isolate_class_specifications(rule)
                            lenClassSpec = len(classSpecification)

                            if lenClassSpec == 2:
                                extendingClass = classSpecification[0]
                                classBeingExtended = classSpecification[1]
                                if app.isInPackageStructure(extendingClass)\
                                        or app.isInPackageStructure(classBeingExtended):
                                    rule = rule + '## is app specific rule ' + app.getName()

                            elif lenClassSpec == 1:
                                classLocationReference = classSpecification[0]
                                if (len(classLocationReference.split('.')) == 1
                                    and classLocationReference.split('.')[0] == '**') \
                                        or (len(classLocationReference.split('.')) == 2
                                            and classLocationReference.split('.')[1] == '**'):
                                    continue
                                if app.isInPackageStructure(classLocationReference):
                                    rule = rule + '## is app specific rule ' + app.getName()
                            else:
                                continue

                            ret.append(rule)
            return ret
        except UnicodeDecodeError:
            print('*************************  unicode decode error: no se puede leer las reglas\n\n' + path + '\n\n')


class AppClass:

    def __repr__(self):
        return self.name + " Class Object"

    def __init__(self, path, app: App):
        self.name = path.split('/')[-1]
        self.path = path
        self.packageLocation = '.'.join(self.path.split('src/main/')[1].split('/')[:-1])
        app.insertClassPackageLocation(self.packageLocation, self.name)
        self.imports = []

    def analyseClass(self, path, imprt, flags, app):
        try:
            # primero se ven los imports de la clase
            with open(path, 'r') as file:
                ret = []
                imports = re.findall(imprt, file.read(), flags(re))

                if imports:
                    for im in imports:
                        ' '.join(im.split())
                        im = im.split(" ")[-1]
                        ret.append(im)
                file.close()

            with open(path, 'r') as file:
                apkResourceLoading = re.findall("\.getResource(AsStream)?\(", file.read(), flags(re))

                if apkResourceLoading:
                    app.insertClassLoadResourceFromAPK(self.packageLocation, self.name)
            self.imports = ret
        except UnicodeDecodeError:
            print('*************************  unicode decode error: no se puede leer ', path)
            return []

    def getImports(self):
        return self.imports


class JavaClass(AppClass):

    def __init__(self, path, app):
        super().__init__(path, app)
        self.analyseClass(path, '^import(.*?);', lambda x: x.MULTILINE | x.DOTALL, app)


class KtClass(AppClass):

    def __init__(self, path, app):
        super().__init__(path, app)
        self.analyseClass(path, '^import(.*?)$', lambda x: x.MULTILINE, app)

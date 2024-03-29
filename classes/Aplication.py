from classes.DBConnect import DBConnect
from pygtrie import StringTrie
from classes.AppClass import *
from classes.ProGuardRuleFile import *
from analysis.AppAnalyser import *
import subprocess
import shutil


class App:
    """
    Clase que modela una app.

    :param path: path de la aplicación.
    """

    def __init__(self, path):
        # se registra el nombre y el path, andemas de los path de los archivos configuradores.
        self.name = path.split('/')[-1]
        self.path = path

        self.analyser = AppAnalyser(self)

        self.buildGradleFiles = self.analyser.findFilePaths(path, "*uild.gradle")
        self.propertiesPaths = self.analyser.findFilePaths(path, "*roject.properties")
        apks = self.analyser.findFilePaths(path, "*.apk")

        self.hasDebugApk = []
        self.originalFilesInApkDir = []
        self.originalDirsInApkDir = []

        for apk in apks:
            if 'build/outputs/apk/' in apk:
                self.hasDebugApk.append(apk)

        self.dontObfuscateRule = False
        self.dontObfuscateFiles = []
        self.classes = []
        self.proguardRuleFiles = []
        self.packageLocations = StringTrie(separator='.')
        self.packageLocationsExtended = StringTrie(separator='.')
        self.classLoadResourceFromAPK = StringTrie(separator='.')
        self.classLoadedByJNIOnNativeSide = StringTrie(separator='.')
        self.dataClasses = StringTrie(separator='.')

        self.obfuscatedDirectories = []

        # se ve si esta activado proguard y donde estan los archivos de reglas
        isObfGradle = self.analyser.isAppObfuscatedG(self.buildGradleFiles)
        isObfProp = self.analyser.isAppObfuscatedP(self.propertiesPaths)

        # Si se existen archivos de reglas en uso, significa que se usa proguard y tiene reglas
        self.isObf = (len(isObfGradle) != 0) or (len(isObfProp) != 0)

        if self.isObf:
            # si esta ofuscado se buscan las reglas y los nombres de las clases

            javaClassesPaths = self.analyser.findFilePaths(path, "*.java")
            ktClassesPaths = self.analyser.findFilePaths(path, "*.kt")

            for pth in javaClassesPaths:
                if 'src/main/java' in pth:
                    self.classes.append(JavaClass(pth, self, 'src/main/java/'))
            for pth in ktClassesPaths:
                if 'src/main/java' in pth:
                    self.classes.append(KtClass(pth, self, 'src/main/java/'))

            proguardRulePaths = []
            for ruleFileName in (isObfProp + isObfGradle):
                proguardRulePaths.extend(self.analyser.findFilePaths(path, ruleFileName))

            for pth in proguardRulePaths:
                file = ProGuard(pth, self)
                self.proguardRuleFiles.append(file)
        # se registran las dependencias
        self.dependencies = self.analyser.extractDependencies(self.buildGradleFiles)
        self.analyser.detectJavaCodeCalledFromNativeInstances()

    def getObfuscatedDirectories(self):
        return self.obfuscatedDirectories

    def insertObfuscatedDirectory(self, dir):
        self.obfuscatedDirectories.append(dir)

    def getRules(self):
        retRules = []
        for pg in self.getPgFiles():
            retRules.extend(pg.getRules())
        retRules = list(set(retRules))
        return retRules

    def getClasses(self):
        return self.classes

    def getDataClasses(self):
        classes = self.classes
        retClasses = []

        for cls in classes:
            if cls.getIsDataClass():
                retClasses.append(cls)

        return retClasses

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

    def saveInDB(self, db: DBConnect):
        appId = db.saveApp(self)
        db.saveDeps(appId, self.getDependencies())
        db.saveRules(appId, self.getRules())
        db.saveImports(appId, self.getAllImports())

    def appendPgFile(self, fileToInclude):
        pgFile = ProGuard(fileToInclude, self)
        self.proguardRuleFiles.append(pgFile)

    def insertDataClassPackageLocation(self, packageLocation, className):
        trie = self.dataClasses

        if packageLocation not in trie.keys():
            trie[packageLocation] = [className]
        else:
            temp = trie.pop(packageLocation)
            temp.append(className)
            trie[packageLocation] = temp

        self.dataClasses = trie

    def getDataClassPackageLocations(self):
        return self.dataClasses

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

    def isInPackageStructureList(self, classLocationReference):
        ret = False
        for clsRef in classLocationReference:
            ret = bool(self.isInPackageStructure(clsRef) or ret)
        return ret

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
        else:
            return False

    def insertClassPackageLocationExtended(self, packageLocation, className):
        trie = self.packageLocationsExtended

        if packageLocation not in trie.keys():
            trie[packageLocation] = [className]
        else:
            temp = trie.pop(packageLocation)
            temp.append(className)
            trie[packageLocation] = temp

        self.packageLocationsExtended = trie

    def getPackageLocationsExtended(self):
        return self.packageLocationsExtended

    def isInPackageStructureExtended(self, classLocationReference):
        separateClassAndElement = classLocationReference.rsplit('.', 1)

        if len(separateClassAndElement) > 1:
            locationReference = separateClassAndElement[0]
            classReference = separateClassAndElement[1]

            packageLocationsTrie = self.getPackageLocationsExtended()

            if classReference == '**' and packageLocationsTrie.has_subtrie(locationReference):
                return True

            elif packageLocationsTrie.has_key(locationReference) \
                    and (classReference+'.java' in packageLocationsTrie[locationReference]
                         or classReference+'.kt' in packageLocationsTrie[locationReference]
                         or classReference == '*'):
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
        unobfuscated_cases = 0

        for key in classes.keys():
            isInDirectory = False
            for dir in self.getObfuscatedDirectories():
                searching = re.sub('\.', '/', key)
                if self.analyser.findFilePaths(dir, searching):
                    isInDirectory = True
            if isInDirectory:
                resourceLoadingClasses = classes[key]
                if key not in allClasses.keys():
                    for clss in resourceLoadingClasses:
                        rule = rulePrefix + key + '.' + clss.split('.', 1)[0] + ruleSuffix
                        if rule not in returnRules:
                            returnRules.append(rule)
                else:
                    classesInSameLocation = allClasses[key]

                    representation = len(resourceLoadingClasses)/len(classesInSameLocation)*100
                    if representation == 100:
                        returnRules.append(rulePrefix + key + ".*" + ruleSuffix)
                    else:
                        for clss in resourceLoadingClasses:
                            rule = rulePrefix + key + '.' + clss.split('.', 1)[0] + ruleSuffix
                            if rule not in returnRules:
                                returnRules.append(rule)
            else:
                unobfuscated_cases += 1
        return returnRules, unobfuscated_cases

    def getRulesForClassesLoadedFromNativeSide(self):
        JNIClasses = self.getClassesLoadedByJNI()
        return self.getRulesForClasses(JNIClasses, "keep, includedescriptorclasses class ", " { *; }")

    def getRulesForDataClasses(self):
        DataClasses = self.getDataClassPackageLocations()
        return self.getRulesForClasses(DataClasses, "keep class ")

    def unpackApk(self, bar, show, verbose):

        if self.hasDebugApk:
            for apk in self.hasDebugApk:

                currentDir = apk.rsplit('/', 1)[0]

                originalContentInApkDir = []
                source = apk.rsplit('/', 1)[0] + '/source'
                sourceDirPresent = False
                for item in os.listdir(currentDir):
                    if item == source: sourceDirPresent = True
                    originalContentInApkDir.append(currentDir + '/' + item)
                if not sourceDirPresent:
                    try:
                        if verbose:
                            bar.text(show + '. Decompressing APK.')
                        with open(os.devnull, 'wb') as devnull:
                            subprocess.check_call(['unzip', '-o', apk, '-d', currentDir], stdout=devnull,
                                                  stderr=subprocess.STDOUT)
                        if verbose:
                            bar.text(show + '. Reformatting Dex file to Jar.')
                        with open(os.devnull, 'wb') as devnull:
                            d2j = '/Volumes/WanShiTong/Archive/UChile/Título/work/tools/dex2jar/2.0/bin/d2j-dex2jar'

                            for folder, dirs, files in os.walk(currentDir):
                                for file in files:
                                    extension = file.rsplit('.', 1)
                                    if len(extension) > 1 and extension[1] == 'dex':
                                        subprocess.check_call([d2j, '-e', currentDir+'errors.zip', '-o', currentDir+'/classes-dex2jar.jar',
                                                               currentDir+'/'+file], stdout=devnull, stderr=subprocess.STDOUT)
                        if verbose:
                            bar.text(show + '. Unpacking Jar.')
                        try:
                            with open(os.devnull, 'wb') as devnull:
                                jdCli = '/Volumes/WanShiTong/Archive/UChile/Título/work/tools/jd-cli-1.2.0-dist/jd-cli.jar'
                                jar = apk.rsplit('/', 1)[0] + '/classes-dex2jar.jar'
                                subprocess.check_call(['java', '-jar', jdCli, jar, '-od', source], stdout=devnull,
                                                      stderr=subprocess.STDOUT, timeout=30)
                        except subprocess.TimeoutExpired:
                            pass
                    except subprocess.CalledProcessError:
                        print('Error en', currentDir)
            if verbose:
                bar.text(show + '. Parsing Extended Classes.')
            javaClassesPaths = self.analyser.findFilePaths(currentDir + '/source', "*.java")
            ktClassesPaths = self.analyser.findFilePaths(currentDir + '/source', "*.kt")

            for pth in javaClassesPaths:
                    self.classes.append(AppClass(pth, self, 'apk/debug/source/', True))
            for pth in ktClassesPaths:
                    self.classes.append(AppClass(pth, self, 'apk/debug/source/', True))
            if verbose:
                bar.text(show + '. Deleting Temporary Files.')
            for item in os.listdir(currentDir):
                item = currentDir + '/' + item
                if item not in originalContentInApkDir and item != source:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                    else:
                        os.remove(item)

        else:
            print(self.name, 'does not have a debug apk. For better results, '
                             'build a debug apk for your project in the standard directory.')

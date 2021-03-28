import glob
import os
import re
import json
from json import JSONEncoder
from classes.DBConnect import DBConnect


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

        # se ve si esta activado proguard y donde estan los archivos de reglas
        isObfGradle = self.isAppObfuscatedG(self.buildGradleFiles)
        isObfProp = self.isAppObfuscatedP(self.propertiesPaths)

        # Si se existen archivos de reglas en uso, significa que se usa proguard y tiene reglas
        self.isObf = (len(isObfGradle) != 0) or (len(isObfProp) != 0)

        if self.isObf:
            # si esta ofuscado se buscan las reglas y los onmbres de las clases
            proguardRulePaths = []
            for ruleFileName in (isObfProp + isObfGradle):
                proguardRulePaths.extend(self.findFilePaths(path, ruleFileName))

            self.proguardRuleFiles = []
            self.rules = []
            for pth in proguardRulePaths:
                file = ProGuard(pth, self)
                self.proguardRuleFiles.append(file)
                self.rules.extend(file.rules.rules)

            javaClassesPaths = self.findFilePaths(path, "*.java")
            ktClassesPaths = self.findFilePaths(path, "*.kt")

            for pth in javaClassesPaths:
                self.classes.append(JavaClass(pth))
            for pth in ktClassesPaths:
                self.classes.append(KtClass(pth))
        # se registran las dependencias
        self.dependencies = self.extractDependencies(self.buildGradleFiles)

    def getRules(self):
        retRules = []
        for pg in self.proguardRuleFiles:
            retRules.extend(pg.getRules())
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
                        if 'exclude' in ln:
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
                            dependencies.extend(re.findall(":(.*?)(?:'|\")", ln))
                        elif 'Libraries' in ln:
                            dependencies.extend(re.findall("\.([-a-zA-Z0-9_]*)\)?", ln))
                        elif 'name:' in ln and 'group:' in ln:
                            dependencies.extend(re.findall("name: *\t*(?:'|\")(.*?)(?:'|\")", ln))
                        else:
                            dependencies.extend(re.findall(":(.*?):", ln))
                        if '}' in ln:
                            if count_bracket == 0:
                                break
                            else:
                                count_bracket -= 1

        ret = list(dict.fromkeys(dependencies).keys())
        if ret is None:
            return[]
        return ret

    def saveInDB(self, db: DBConnect):
        appId = db.saveApp(self)
        db.saveDeps(appId, self.getDependencies())
        db.saveRules(appId, self.getRules())
        db.saveImports(appId, self.getAllImports())


class Rules:

    def __init__(self, rules):
        self.rules = rules


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
    def findFileRules(self, path, app):
        try:
            with open(path, 'r') as file:
                ret = []
                opened_rule = re.sub(r'(?m)^\s*#.*\n?', '', file.read())
                opened_rule = ' '.join(opened_rule.split())
                opened_rule = opened_rule.split("-")[1:]
                pattern = re.compile('[^a-zA-Z0-9_*.,;<>(){}@ -]+')
                if opened_rule:
                    for rule in opened_rule:
                        if "dontobfuscate" in rule:
                            app.dontObfuscateRule = True
                            app.dontObfuscateFiles.append(path)
                            return []
                        ret.append(pattern.sub('', rule.replace("\\n", "").replace("\\r", "")))
            return ret
        except UnicodeDecodeError:
            print('*************************  unicode decode error: no se puede leer las reglas\n\n' + path + '\n\n')


class CostumFileEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class AppClass:

    def __repr__(self):
        return self.name + " Class Object"

    def __init__(self, path):
        self.name = path.split('/')[-1]
        self.path = path
        self.imports = []

    def findImports(self, path, imprt, flags):
        try:
            with open(path, 'r') as file:
                ret = []

                imports = re.findall(imprt, file.read(), flags(re))

                if imports:
                    for im in imports:
                        ' '.join(im.split())
                        im = im.split(" ")[-1]
                        ret.append(im)
            return ret
        except UnicodeDecodeError:
            print('*************************  unicode decode error: no se puede leer las reglas')
            return []

    def getImports(self):
        return self.imports


class JavaClass(AppClass):

    def __init__(self, path):
        super().__init__(path)
        self.imports = self.findImports(path, '^import(.*?);', lambda x: x.MULTILINE | x.DOTALL)


class KtClass(AppClass):
    def __init__(self, path):
        super().__init__(path)
        self.imports = self.findImports(path, '^import(.*?)$', lambda x: x.MULTILINE)

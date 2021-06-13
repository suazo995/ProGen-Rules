import os
from classes.DBConnect import DBConnect
from pygtrie import StringTrie
from classes.AppClass import *
from classes.ProGuardRuleFile import *
from classes.AppAnalyser import *


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

        self.dontObfuscateRule = False
        self.dontObfuscateFiles = []
        self.classes = []
        self.proguardRuleFiles = []
        self.packageLocations = StringTrie(separator='.')
        self.classLoadResourceFromAPK = StringTrie(separator='.')
        self.classLoadedByJNIOnNativeSide = StringTrie(separator='.')

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
                if 'src/main/' in pth:
                    self.classes.append(JavaClass(pth, self))
            for pth in ktClassesPaths:
                if 'src/main/' in pth:
                    self.classes.append(KtClass(pth, self))

            proguardRulePaths = []
            for ruleFileName in (isObfProp + isObfGradle):
                proguardRulePaths.extend(self.analyser.findFilePaths(path, ruleFileName))

            for pth in proguardRulePaths:
                file = ProGuard(pth, self)
                self.proguardRuleFiles.append(file)
        # se registran las dependencias
        self.dependencies = self.analyser.extractDependencies(self.buildGradleFiles)
        self.analyser.detectJavaCodeCalledFromNativeInstances()

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

    def saveInDB(self, db: DBConnect):
        appId = db.saveApp(self)
        db.saveDeps(appId, self.getDependencies())
        db.saveRules(appId, self.getRules())
        db.saveImports(appId, self.getAllImports())

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

    def getRulesForClassesLoadedFromNativeSide(self):
        JNIClasses = self.getClassesLoadedByJNI()
        return self.getRulesForClasses(JNIClasses, "keep, includedescriptorclasses class ", " { *; }")



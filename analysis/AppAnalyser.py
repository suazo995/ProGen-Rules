import glob
import re
import os


class AppAnalyser:

    def __init__(self, app):
        self.app = app

    @staticmethod
    def findFilePaths(path, file):
        return glob.glob(path + "/**/" + file, recursive=True)

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

                        if '}' in ln:
                            if count_bracket == 0:
                                break
                            else:
                                count_bracket -= 1

                        if 'fileTree' in ln:
                            if 'dir' in ln:
                                search = "dir: '(.*?)'"
                            else:
                                search = "'(.*?)'"
                            for direct in re.findall(search, ln):
                                self.app.insertObfuscatedDirectory(file.rsplit('/', 1)[0])
                                ruleFiles.extend(os.listdir('/'.join(file.split('/')[0:-1]) + "/" + direct))
                        else:
                            self.app.insertObfuscatedDirectory(file.rsplit('/', 1)[0]+'/src/main/java/')
                            ruleFiles.extend(re.findall("'(.*?\..*?)'", ln))
        return ruleFiles

    @staticmethod
    def openPropertiesFile(file, encoding='utf-8'):
        ruleFiles = []
        with open(file, 'r', encoding=encoding) as myFile:
            for line in myFile:
                ln = line.split("#")[0].split("!")[0]
                if 'proguard.config' in ln:
                    ln = ln.split('=')[1].split(":")
                    for l in ln:
                        ruleFilesNames = re.findall('(.*?\.txt)', l.split("\\")[-1])
                        if ruleFilesNames:
                            for rf in ruleFilesNames:
                                ruleFiles.append(rf)
        return ruleFiles

    @staticmethod
    def isAppObfuscatedP(prop):
        ruleFiles = []
        for file in prop:
            try:
                ruleFiles.extend(AppAnalyser.openPropertiesFile(file))
            except UnicodeDecodeError:
                ruleFiles.extend(AppAnalyser.openPropertiesFile(file, 'iso-8859-15'))
        return ruleFiles

    @staticmethod
    def extractDependencies(build):
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

    def rulesForDepInApp(self, dep, prnt=False, f=None):
        """
            Entrega las reglas para una dependencia en específico.

            :param app: Objeto analisador de una app, dep: Nombre de la dependencia.
            :return: lista de reglas atinentes a la dependencia.
        """
        app = self.app
        imports = app.getAllImports()
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

        for pg in app.getPgFiles():
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

            :param app: Objeto analisador de una app.
            :return: lista de reglas atinentes a las dependencias de la app.
        """
        rulesForDeps = []
        app = self.app

        for dep in app.dependencies:
            rulesForDeps.extend(app.analyser.rulesForDepInApp(dep)[0])

        return rulesForDeps

    @staticmethod
    def JNIHeuristics(fullpath, JNIClassCall, includeJNIDeclaration, JNIEnvDeclaration, encoding='utf-8'):
        f = open(fullpath, 'r', encoding=encoding)
        returnClasses = []
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
        f.close()

        f = open(fullpath, 'r', encoding=encoding)
        if (JNIClassCall and includeJNIDeclaration) or JNIEnvDeclaration:
            match = re.findall("\"([a-zA-Z0-9_]+?/[a-zA-Z0-9_]+?[a-zA-Z0-9/_]*?)\"", f.read(), re.MULTILINE)
            if match:
                returnClasses.extend(match)
        f.close()
        return returnClasses

    def detectJavaCodeCalledFromNativeInstances(self):
        returnClasses = []

        app = self.app

        for folder, dirs, files in os.walk(app.path):
            for file in files:
                JNIClassCall = False
                JNIEnvDeclaration = False
                includeJNIDeclaration = False

                fullpath = os.path.join(folder, file)
                extension = fullpath.rsplit('.', 1)[-1]

                if extension == "cpp" or extension == "c":
                    try:
                        returnClasses.extend(AppAnalyser.JNIHeuristics(fullpath, JNIClassCall, includeJNIDeclaration, JNIEnvDeclaration))
                    except UnicodeDecodeError:
                        returnClasses.extend(AppAnalyser.JNIHeuristics(fullpath, JNIClassCall, includeJNIDeclaration, JNIEnvDeclaration, encoding='iso-8859-15'))
                    except FileNotFoundError:
                        print('File Not Found:', fullpath.split('obfApps')[1])

        reformatClasses = list(map(lambda x: x.replace('/', '.'), returnClasses))
        for clss in reformatClasses:
            clssSplit = clss.rsplit('.', 1)
            packageLocation = clssSplit[0]
            className = clssSplit[1]
            app.insertClassLoadedByJNI(packageLocation, className)

    def detectDataClasses(self, prnt=False):
        app = self.app
        classes = app.getClasses()

        dataClasses = []

        for cls in classes:
            if cls.analyser.detectDataClass():
                dataClasses.append(cls)

        return dataClasses

    def appSpecificRules(self):
        ret = []
        rls = self.app.getRules()
        for r in rls:
            if "## is app specific" in r:
                ret.append(r)
        return ret

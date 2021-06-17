import re
from classes.AppClassAnalyser import *


class AppClass:

    def __repr__(self):
        return self.name + " Class Object"

    def __init__(self, path, app, separator, extended):
        self.name = path.split('/')[-1]
        self.path = path
        self.packageLocation = '.'.join(self.path.split(separator)[1].split('/')[:-1])
        if not extended:
            app.insertClassPackageLocation(self.packageLocation, self.name)
        else:
            app.insertClassPackageLocationExtended(self.packageLocation, self.name)
        self.imports = []
        self.isDataClass = False

        try:
            f = open(path, 'r')
        except UnicodeDecodeError:
            f = open(path, 'r', encoding='iso-8859-15')
        self.code = f.read()
        f.close()

    def getCode(self):
        return self.code

    def analyseClass(self, path, imprt, flags, app, is_kt=False):
        try:
            # primero se ven los imports de la clase
            file = self.code
            ret = []
            imports = re.findall(imprt, file, flags(re))

            if imports:
                for im in imports:
                    ' '.join(im.split())
                    im = im.split(" ")[-1]
                    ret.append(im)

            apkResourceLoading = re.findall("\.getResource(AsStream)?\(", file, flags(re))

            if is_kt:
                self.isDataClass = bool(re.findall("^data class .+?\(", file, flags(re)))

            if apkResourceLoading:
                app.insertClassLoadResourceFromAPK(self.packageLocation, self.name)

            self.imports = ret
        except UnicodeDecodeError:
            print('*************************  unicode decode error: no se puede leer ', path)
            return []

    def getImports(self):
        return self.imports

    def isDataClass(self):
        return self.isDataClass


class JavaClass(AppClass):

    def __init__(self, path, app, separator, extended=False):
        super().__init__(path, app, separator, extended)
        self.analyseClass(path, '^import(.*?);', lambda x: x.MULTILINE | x.DOTALL, app)
        self.analyser = AppClassAnalyser(self)
        try:
            self.isDataClass = self.analyser.detectDataClass()
        except javalang.parser.JavaSyntaxError:
            if 'apk/debug/source/' not in path: print(path)


class KtClass(AppClass):

    def __init__(self, path, app, separator, extended=False):
        super().__init__(path, app, separator, extended)
        self.analyseClass(path, '^import(.*?)$', lambda x: x.MULTILINE, app, True)

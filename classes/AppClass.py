from analysis.AppClassAnalyser import *


class AppClass:

    def __repr__(self):
        return self.name + " Class Object"

    def __init__(self, path, app, separator, extended):
        self.analyser = AppClassAnalyser(self)
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

    def getPackageLocation(self):
        return self.packageLocation

    def getName(self):
        return self.name

    def getCode(self):
        return self.code

    def setImports(self, imports):
        self.imports = imports

    def getImports(self):
        return self.imports

    def setIsDataClass(self, isit):
        self.isDataClass = isit

    def getIsDataClass(self):
        return self.isDataClass


class JavaClass(AppClass):

    def __init__(self, path, app, separator, extended=False):
        super().__init__(path, app, separator, extended)
        self.analyser.analyseClass(self, path, '^import(.*?);', lambda x: x.MULTILINE | x.DOTALL, app)
        try:
            self.setIsDataClass(self.analyser.detectDataClass())
        except javalang.parser.JavaSyntaxError:
            if 'apk/debug/source/' not in path: print(path)

        if self.isDataClass:
            app.insertDataClassPackageLocation(self.packageLocation, self.name)


class KtClass(AppClass):

    def __init__(self, path, app, separator, extended=False):
        super().__init__(path, app, separator, extended)
        self.analyser.analyseClass(self, path, '^import(.*?)$', lambda x: x.MULTILINE, app, True)

        if self.isDataClass:
            app.insertDataClassPackageLocation(self.packageLocation, self.name)

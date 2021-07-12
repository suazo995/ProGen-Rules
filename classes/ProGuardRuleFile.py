from analysis.ProGuardAnalyser import *


class ProGuard:
    """
    Clase que modela un archivo proguard.
    """

    def __init__(self, path, app):
        self.name = path.split('/')[-1]
        self.path = path
        self.defaultFile = (self.name == 'proguard-rules.pro')
        self.analyser = ProGuardAnalyser()
        self.rules = Rules(self.analyser.findFileRules(path, app))

    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def getRules(self):
        return self.rules.rules

class Rules:

    def __init__(self, rules):
        self.rules = rules
import os
import random
from alive_progress import alive_bar
from classes.Aplication import App
from classes.DBConnect import *


class FDroid:

    # Al inicializar una repo usar Fdroid(path, True) para guardar en la BD
    def __init__(self, path='', save=False):
        directories = os.listdir(path)

        self.path = path
        self.apps = []
        self.appsObfuscated = []
        self.appsUnObfuscated = []
        self.appsObfuscatedWithoutDontOfRule = []

        if save:
            self.base = DBConnect()

        with alive_bar(len(directories)) as bar:
            for item in directories:
                bar('Processing: ' + item)
                app = App(self.path + "/" + item)

                self.apps.append(app)

                if app.isObfuscated():
                    if save:
                        app.saveInDB(self.base)
                    self.appsObfuscated.append(app)
                    if not app.dontObfuscateRule:
                        self.appsObfuscatedWithoutDontOfRule.append(app)
                else:
                    self.appsUnObfuscated.append(app)
        if save:
            self.base.close()

    def initFromList(self, appList):
        for app in appList:
            self.apps.append(app)

    def numberOfApps(self):
        return len(self.apps)

    def obfuscatedApps(self):
        return self.appsObfuscated

    def numObfuscatedApps(self):
        return len(self.obfuscatedApps())

    def unObfuscatedApps(self):
        return self.appsUnObfuscated

    def numUnObfuscatedApps(self):
        return len(self.unObfuscatedApps())

    def randomApp(self):
        return random.choice(self.apps)

    def randomObfuscated(self):
        return random.choice(self.appsObfuscated)

    def randomNotObfuscated(self):
        return random.choice(self.appsUnObfuscated)

    def randomObfuscatedDontWarn(self):
        return random.choice(self.ofAppsWithoutDontOfRule())

    def propertiesFileApp(self):
        ret = []
        for app in self.obfuscatedApps():
            if app.propertiesPaths:
                ret.append(app)
        return ret

    def getApps(self):
        return self.apps

    def ofAppsWithoutDontOfRule(self):
        return self.appsObfuscatedWithoutDontOfRule

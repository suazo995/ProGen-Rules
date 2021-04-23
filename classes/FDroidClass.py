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
        self.appsOfuscadas = []
        self.appsNoOfuscadas = []
        self.appsOfuscadasSinDontOf = []

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
                    self.appsOfuscadas.append(app)
                    if not app.dontObfuscateRule:
                        self.appsOfuscadasSinDontOf.append(app)
                else:
                    self.appsNoOfuscadas.append(app)
        if save:
            self.base.close()

    def initFromList(self, appList):
        for app in appList:
            self.apps.append(app)

    def numberOfApps(self):
        return len(self.apps)

    def obfuscatedApps(self):
        return self.appsOfuscadas

    def numObfuscatedApps(self):
        return len(self.obfuscatedApps())

    def unObfuscatedApps(self):
        return self.appsNoOfuscadas

    def numUnObfuscatedApps(self):
        return len(self.unObfuscatedApps())

    def randomApp(self):
        return random.choice(self.apps)

    def randomObfuscated(self):
        return random.choice(self.appsOfuscadas)

    def randomNotObfuscated(self):
        return random.choice(self.appsNoOfuscadas)

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
        return self.appsOfuscadasSinDontOf

from classes.AppClass import *
import re
import collections
from classes.FDroidClass import FDroid
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

"""
    Clase que analisa una aplicación dada
    
    :param app: un objeto App.

"""
class AppAnalyser:

    def __init__(self, app: App):
        self.app = app

    def rulesForDepInApp(self, dep):
        """
            Entrega las reglas para una dependencia en específico.

            :param self: Objeto analisador de una app, dep: Nombre de la dependencia.
            :return: lista de reglas atinentes a la dependencia.
        """

        imports = self.app.getAllImports()
        relatedImports = []

        for im in imports:
            if dep in im:
                relatedImports.append(im.split(".")[-1])

        rulesForThisDep = []

        for pg in self.app.proguardRuleFiles:
            for rule in pg.getRules():
                if dep in rule:
                    rulesForThisDep.append(rule)
                else:
                    for im in relatedImports:
                        if im in rule:
                            rulesForThisDep.append(rule)

        return rulesForThisDep


    def rulesForDeps(self):
        """
            Entrega las reglas para todas las dependencias de la app.

            :param self: Objeto analisador de una app.
            :return: lista de reglas atinentes a las dependencias de la app.
        """
        rulesForDeps = []

        for dep in self.app.dependencies:
            rulesForDeps.extend(self.rulesForDepInApp(dep))

        return rulesForDeps
"""
    def rulesForImports(self):
        rulesForImp = []

        for cl in self.app.classes:
            if cl.imports:

                for im in cl.imports:
                    for pg in self.app.proguardRuleFiles:
                        for rule in pg.rules.rules:

                            try:
                                match = re.search(im, rule)
                                if match:
                                    rulesForImp.append({"Import": im, "Rule": rule, "App": cl.name})
                                    print({"Import": im, "Rule": rule, "App": cl.name})
                            except re.error:
                                pass
            else:
                pass
        return rulesForImp
"""






class FDroidAnalyser:
    """
        Clase analisadora de un conjunto de aplicaciones.

        :param fdroid: un objeto tipo FDroid.
    """

    def __init__(self, fdroid: FDroid):
        self.repo = fdroid


    def distinctRulesPerDep(self):
        """
            Grafica el numero de reglas por Dependencia.
        """
        apps = self.repo.obfuscatedApps()
        ret = {}

        for app in apps:
            for dnr in AppAnalyser(app).rulesForDeps():
                for rule in dnr[1]:
                    try:
                        if rule not in ret[dnr[0]]:
                            ret[dnr[0]] = ret[dnr[0]].append(rule)
                    except (KeyError, TypeError):
                        ret[dnr[0]] = [rule]

        count = []
        for value in ret.values():
            count.append(len(value))

        plt.style.use('ggplot')
        plt.hist(count, histtype="bar")
        plt.xlabel("Number of rules")
        plt.ylabel("Dependency")
        plt.title("Total Number of Dependencies per App", loc='center', wrap=True)
        plt.tight_layout()
        plt.show()



    def numberOfRules(self):
        """
            Grafica el numero de reglas por App.
        """
        count = []

        apps = self.repo.obfuscatedApps()
        for app in apps:
            count.append(app.getNumberOfRules())
        plt.style.use('ggplot')
        plt.hist(count, histtype="bar", bins=range(min(count) + 1, int(sum(count)/len(count))*2, 1), color='#0504aa',
                            alpha=0.7, rwidth=0.85)

        plt.xticks(range(min(count) + 1, int(sum(count) / len(count)) * 2, 5))
        plt.tight_layout()

        plt.xlabel("Number of rules")
        plt.ylabel("Apps")
        plt.title("Number of Rules per App", loc='center', wrap=True, pad=2)
        plt.show()


    def obfVsSinObf(self):
        """
            Visualizacion de la cantidad de apps con y sin ofuscación.
        """
        labels = 'Ofuscadas', 'No ofuscadas'
        plt.style.use('ggplot')
        plt.pie([self.repo.numObfuscatedApps(), self.repo.numUnObfuscatedApps()], explode=(0, 0.1),
                labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        plt.show()


    def obfWithDontObf(self):
        """
            Visualizacion de la cantidad de apps con regla dontObfuscate.
        """
        count = 0
        for app in self.repo.obfuscatedApps():
            if app.getDontObfuscateRule():
                count += 1
        labels = 'Sin -do', 'Con -do'
        plt.style.use('ggplot')
        plt.pie([self.repo.numObfuscatedApps() - count, count], explode=(0, 0.1),
                labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        plt.show()


    def dependenciesHistogram(self):
        """
            Histograma de la cantidad de dependencias por app.
        """

        numOfDepsPerApp = []
        for app in self.repo.apps:
            numOfDepsPerApp.append(len(app.getDependencies()))
        plt.style.use('ggplot')
        plt.hist(numOfDepsPerApp, histtype="bar", bins=range(min(numOfDepsPerApp) +1, int(sum(numOfDepsPerApp)/len(numOfDepsPerApp))*2, 1), color='#0504aa',
                            alpha=0.7, rwidth=0.85)

        plt.xticks(range(min(numOfDepsPerApp) + 1, int(sum(numOfDepsPerApp) / len(numOfDepsPerApp)) * 2, 5))
        plt.tight_layout()

        plt.xlabel("Number of Dependencies")
        plt.ylabel("Apps")
        plt.title("Number of Dependencies per App", loc='center', wrap=True, pad=2)
        plt.show()


    def depRuleHistogram(self):
        """
            Histograma de la cantidad de reglas por dependencias por app.
        """

        numberOfRules = []

        for app in self.repo.obfuscatedApps():
            analyser = AppAnalyser(app)
            for dep in app.getDependencies():
                numberOfRules.append(len(analyser.rulesForDepInApp(dep)))

        plt.style.use('ggplot')
        plt.hist(numberOfRules, histtype="bar", bins=range(min(numberOfRules) + 1, 46, 1), color='#0504aa',
                            alpha=0.7, rwidth=0.85)

        plt.xticks(range(min(numberOfRules) + 1, 46, 5))
        plt.tight_layout()

        plt.xlabel("Number of Rules")
        plt.ylabel("Dependencies")
        plt.title("Number of Rules per Dependency on an App", loc='center', wrap=True, pad=2)
        plt.show()


    """
    def repeatedRulesPerImport(self, times: int):

        rulesForEachImort = []

        for app in self.repo.appsOfuscadas:
            analyser = AppAnalyser(app)

            rulesForEachImort.extend(analyser.rulesForImports())

        impWithAllRules = {}

        for tuple in rulesForEachImort:
            imp = tuple["Import"]
            rule = tuple["Rule"]
            app = tuple["App"]

            if imp not in impWithAllRules:

                impWithAllRules[imp] = [rule]
                for tupleAux in rulesForEachImort:
                    if tupleAux["Import"] == imp and tupleAux["App"] != app:

                        placeHolder = [].extend(impWithAllRules[imp])
                        impWithAllRules[imp] = placeHolder.append(tupleAux["Rule"])

        impWithRepeatedRules = {}

        for imp, rules in impWithAllRules.items():
            impWithRepeatedRules[imp] = [rule for rule, count in ºº.Counter(rules).items() if count > times]

        return impWithAllRules, impWithRepeatedRules
    """

    def sameDepNumDeps(self):
        """
            Ordena las apps ofuscadas y no ofuscadas por numero de dependencias y busca parejas que tengan bajo numero
            de dependencias, compartan una dependencia y que una este ofuscada y la otra no. Esto para ver si al usar todas
            las reglas de una dependencia ofuscada en una sin ofuscar, se puede prender la ofuscacion sin problemas

            :param self: Objeto analisador de la repo fdroid.
            :return: null. Se imprime un archivo de texto con los resultados
        """
        ofApps = self.repo.ofAppsWithoutDontOfRule()

        f = open("sharedDeps.txt", "w")

        for of_app in ofApps:
            if len(of_app.rules) > 0:
                f.write(of_app.name + "\n")
                deps = of_app.getDependencies()
                for dep in deps:
                    for non_of_app in ofApps:
                        if non_of_app.name != of_app.name and   dep in non_of_app.getDependencies():
                            f.write("\t" + non_of_app.name + ": " + dep + "\n")
        f.close()

    def mostUsedDeps(self):
        """
            Entrega las dependencias mas usadas de la repo

            :param self: Objeto analisador de la repo fdroid.
            :return: null. Se imprime un archivo de texto con los resultados
        """
        apps = self.repo.ofAppsWithoutDontOfRule()

        totalDeps = []

        for app in apps:
            appAn = AppAnalyser(app)
            deps = app.getDependencies()
            for dep in deps:
                if "'org.bouncycastle', name" in dep:
                    print(app.name)
                totalDeps.append(dep)

        depsTimesUesed = dict.fromkeys(totalDeps, 0)

        for dep in totalDeps:
            depsTimesUesed[dep] += 1

        ret = {k: v for k, v in sorted(depsTimesUesed.items(), key=lambda item: item[1], reverse=True)}

        f = open("mostUsedDeps.txt", "w")

        for key in ret:
            f.write(key + ":\t\t\t" + str(ret[key]) + "\n")
        f.close()

    def mostRulesDeps(self):
        """
            Entrega las reglas mas usadas de la repo

            :param self: Objeto analisador de la repo fdroid.
            :return: null. Se imprime un archivo de texto con los resultados
        """
        apps = self.repo.ofAppsWithoutDontOfRule()

        totalDeps = []
        depRules = []

        for app in apps:
            appAn = AppAnalyser(app)

            deps = app.getDependencies()
            for dep in deps:
                depRules.append(appAn.rulesForDepInApp(dep))
                totalDeps.append(dep)

        depsRulesUsed = dict.fromkeys(totalDeps, 0)

        count = 0
        for dep in totalDeps:
            depsRulesUsed[dep] += len(depRules[count])
            count += 1

        ret = {k: v for k, v in sorted(depsRulesUsed.items(), key=lambda item: item[1], reverse=True)}

        f = open("mostRulesDeps.txt", "w")

        for key in ret:
            f.write(key + ":\t\t\t" + str(ret[key]) + "\n")
        f.close()

    def appsThatUseDep(self, dep):
        """
            Entrega las apps que usan determinada dependencia

            :param self: Objeto analisador de la repo fdroid, dep: nombre de una dependencia.
            :return: null. Se imprime un archivo de texto con los resultados
        """
        apps = self.repo.ofAppsWithoutDontOfRule()
        ret = []

        for app in apps:
            if dep in app.getDependencies():
                ret.append(app)

        f = open("appsThatUse_" + dep + ".txt", "w")
        f.write("App\t\t\tNumber of Rules\n")

        for app in ret:
            rulesForDep = AppAnalyser(app).rulesForDepInApp(dep)
            f.write(app.getName()+"\t\t\t"+str(len(rulesForDep))+"\n")
        f.close()

    def rulesForDepExcludingApp(self, dep, appName, prnt=False):
        """
            Entrega todas las reglas para determinada dependencia de una app determinada excluyendo las reglas propias.

            :param self: Objeto analisador de la repo fdroid, dep: nombre de una dependencia, appName: Nombre de la app,
            prnt: bool para ver si registra los archivos.
            :return: null. Se imprime un archivo de texto con los resultados
        """
        apps = self.repo.ofAppsWithoutDontOfRule()

        returnRules = []
        if prnt: f = open("generatedRulesFor_" + appName + "_Dep_" + dep + ".txt", "w")

        for app in apps:
            if app.getName() == appName:
                continue
            elif dep in app.getDependencies():

                rules = AppAnalyser(app).rulesForDepInApp(dep)
                if len(rules) > 0 and prnt: f.write("# " + app.name + "\n")
                for rule in rules:
                    if rule not in returnRules:
                        returnRules.append(rule)
                        if prnt: f.write("-"+rule+"\n")
        if prnt: f.close()
        return returnRules


    def rulesForAllDepsExcludingApp(self, application: App, prnt=False):
        """
            Entrega todas las reglas para todas las dependencias de una app excluyendo las reglas de la app determinada.

            :param self: Objeto analisador de la repo fdroid, application: Nombre de la app,
            prnt: bool para ver si registra los archivos.
            :return: null. Se imprime un archivo de texto con los resultados
        """
        apps = self.repo.ofAppsWithoutDontOfRule()

        returnRules = []

        if prnt: f = open("generatedRulesFor_" + application.getName() + "_dependencies.txt", "w")

        dependencies = application.getDependencies()

        for app in apps:
            if app.getName() == application.getName():
                continue
            else:
                for dep in dependencies:
                    if dep in app.getDependencies():
                        rules = AppAnalyser(app).rulesForDepInApp(dep)
                        for rule in rules:
                            if rule not in returnRules:
                                returnRules.append(rule)
                                if prnt: f.write("-" + rule + "\n")
        if prnt: f.close()
        return returnRules

    def rulesForAllDepsList(self, apps: [App], prnt=False):
        """
            Entrega las reglas para las dependencias de una lista de aplicaciones.

            :param self: Objeto analisador de la repo fdroid, apps: lista de aplicaciones ,prnt: bool para ver si
            registra los archivos.
            :return: Lista de reglas. Se imprime un archivo de texto con los resultados
        """
        totalRules = []

        for app in apps:
            totalRules.append(self.rulesForAllDepsExcludingApp(app, prnt))

        return totalRules

import os
import re

from classes.Aplication import App
from classes.DBConnect import DBConnect
from analysis.ProGuardAnalyser import isolate_class_references


class DataBaseAnalyser:
    def __init__(self, database: DBConnect):
        self.database = database

    def rulesForAllDepsExcludingApp(self, application: App, percentage = 25, prnt=False, checkApk=False):
        """
            Entrega todas las reglas para todas las dependencias de una app excluyendo las reglas de la app determinada.

            :param self: Objeto analisador de la repo fdroid, application: Nombre de la app,
            prnt: bool para ver si registra los archivos.
            :return: null. Se imprime un archivo de texto con los resultados
        """
        dependencies = application.getDependencies()
        appsAndRules = self.database.getAppsWithDeps(dependencies)

        if prnt:
            path = "resultsDB/" + application.getName()
            if not os.path.exists(path):
                os.makedirs(path)
            f = open(path + "/RulesFor_" + application.getName() + "_dependencies.pro", "w")
        else:
            f = None

        returnRules = []
        negativeRules = []
        compRules = []
        appsWithDep = dict.fromkeys(dependencies, 0)

        for tuple in appsAndRules:
            app = tuple[0]
            appDeps = tuple[1].split('%')
            rules = tuple[2].split('%')
            imports = tuple[3].split('%')

            lastRuleForDepSeenIndx = -1

            if app == application.getName():
                continue

            try:
                for depen in appDeps:
                    appsWithDep[depen] += 1
            except KeyError:
                print('oops')

            else:
                if prnt and rules:
                    f.write("\n# Rules from App: " + app + "\n")

                for idx, rule in enumerate(rules):
                    for dep in appDeps:
                        if dep in dependencies:
                            if dep in rule:
                                if prnt: f.write("-" + rule + "\t# por " + dep + "\n")
                                if rule not in returnRules:
                                    returnRules.append(rule)
                                lastRuleForDepSeenIndx = idx
                                break

                            elif rule not in returnRules:
                                if lastRuleForDepSeenIndx != -1 and (idx - lastRuleForDepSeenIndx) <= 4:
                                    if prnt: f.write("-" + rule + "\t# por proximidad\n")
                                    returnRules.append(rule)
                                else:
                                    for indx, im in enumerate(imports):

                                        importEnd = im.split(".")[-1]
                                        if importEnd == "*" or importEnd == "**" and im.split(".")[-2] != "":
                                            continue

                                        if re.findall('\.'+importEnd+'\.?', rule):
                                            if prnt: f.write("-" + rule + "\t# del import: " + im + "\n")
                                            returnRules.append(rule)
                                            break
                                        elif indx == len(imports)-1:
                                            compRules.append((rule, dep))
                                            break

        rulesTimesUsed = dict.fromkeys(compRules, 0)

        for tuple in compRules:
            rulesTimesUsed[tuple] += 1

        compRulesSorted = {k: v for k, v in sorted(rulesTimesUsed.items(), key=lambda item: item[1], reverse=True)}

        if prnt: f.write("\n# Reglas Acompañantes (presentes en > " + str(percentage) + " )" + "\n")

        rulePerc = {}

        for key in compRulesSorted:
            rule = key[0]
            dep = key[1]

            frec = compRulesSorted[key]
            perc = (frec/appsWithDep[dep])*100

            if rule in rulePerc.keys():
                currentPerc = rulePerc[rule]
                if perc > currentPerc:
                    rulePerc[rule] = perc
            elif perc >= percentage:
                rulePerc[rule] = perc

        for key in rulePerc:
            rule = key
            perc = rulePerc[key]
            if prnt: f.write("-" + rule + "\t # presente en  " + str(round(perc, 2)) + "%" + "\n")
            if rule not in returnRules:
                returnRules.append(rule + "# presente en  " + str(round(perc, 2)) + "%")

        for tup in compRules:
            rule = tup[0]
            inRet = False
            if rule not in negativeRules:
                for r in returnRules:
                    if rule == r.split('#')[0]:
                        inRet = True
                        break
                if not inRet: negativeRules.append(rule)

        positiveRules = []

        if application.hasDebugApk and checkApk:
            for retR in returnRules:
                isInPackageStructure = True

                classSpecifications = isolate_class_references(retR)[0]
                for clsSpec in classSpecifications:
                    if clsSpec == '*' or clsSpec == '**' or 'java.' in clsSpec or 'javax.' in clsSpec:
                        isInPackageStructure = isInPackageStructure and True
                        continue
                    isInPackageStructure = isInPackageStructure and application.isInPackageStructureExtended(clsSpec)

                if isInPackageStructure or 'keep' not in retR.split(' ', 1)[0]:
                    positiveRules.append(retR)
                else:
                    negativeRules.append(retR)
        else:
            positiveRules.extend(returnRules)

        if prnt: f.close()
        return positiveRules, negativeRules

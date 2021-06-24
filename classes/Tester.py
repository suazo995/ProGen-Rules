import sys
from alive_progress import alive_bar
from classes.FDroidClass import FDroid
from classes.Aplication import App, isolate_class_specifications
from classes.DBConnect import DBConnect
from analysis.fdroidAnalyser import FDroidAnalyser, DataBaseAnalyser

sys.path.insert(1, '/Volumes/WanShiTong/Archive/UChile/Título/work/Src')


def is_subgroup_of_class_spec(candidate, original):

    head_original, *tail_original = original
    head_candidate, *tail_candidate = candidate

    end_of_candidate = not bool(tail_candidate)
    end_of_original = not bool(tail_original)

    if head_candidate == "*":
        if end_of_candidate and end_of_original:
            return True
        elif head_original == "**":
            if not end_of_candidate and not end_of_original:
                if tail_original[0] == tail_candidate[0]:
                    return is_subgroup_of_class_spec(tail_candidate, tail_original)
                else:
                    return is_subgroup_of_class_spec(tail_candidate, original)
            if end_of_candidate:
                if not end_of_original:
                    return is_subgroup_of_class_spec(candidate, tail_original)
                return False
        elif end_of_candidate and not end_of_original:
            return False
        return is_subgroup_of_class_spec(tail_candidate, tail_original)
    elif head_candidate == "**":
        if head_original == '*':
            if end_of_original and end_of_candidate:
                return False
        if head_original == "**" and not end_of_original and not end_of_candidate \
                and tail_original[0] == tail_candidate[0]:
            return is_subgroup_of_class_spec(tail_candidate, tail_original)
        if end_of_candidate:
            return True
        if not end_of_candidate and not end_of_original:
            if tail_original[0] == tail_candidate[0]:
                return is_subgroup_of_class_spec(tail_candidate, tail_original)
            else:
                return is_subgroup_of_class_spec(candidate, tail_original)
    else:
        if head_original == "**":
            if not end_of_candidate and not end_of_original:
                if tail_original[0] == tail_candidate[0]:
                    return is_subgroup_of_class_spec(tail_candidate, tail_original)
                else:
                    return is_subgroup_of_class_spec(tail_candidate, original)
            if end_of_original and not end_of_candidate:
                return False
            if end_of_candidate:
                return False
        elif head_original == head_candidate:
            if end_of_candidate and end_of_original:
                return True
            return is_subgroup_of_class_spec(tail_candidate, tail_original)
        if head_original == '*' and not end_of_candidate and not end_of_original:
            return is_subgroup_of_class_spec(tail_candidate, tail_original)
        else:
            return False


def is_equivalent_rule(original, candidate):
    try:
        class_specification_rules = ['keep', 'keepclassmembers', 'keepclasseswithmembers', 'keepnames',
                                     'keepclassmembernames', 'keepclasseswithmembernames', 'dontwarn', 'dontnote']
        if original.split(' ', 1)[0].split(',', 1)[0] in class_specification_rules:
            class_spec_original = isolate_class_specifications(original)
            class_spec_candidate = isolate_class_specifications(candidate)

            original_split_list = original.split()
            candidate_split_list = candidate.split()

            if len(original_split_list) == len(candidate_split_list) \
                    and len(class_spec_candidate) == len(class_spec_original):
                for index, segment_original in enumerate(original_split_list):
                    segment_candidate = candidate_split_list[index]
                    if segment_original in class_spec_original and segment_candidate in class_spec_candidate:
                        candidate_class_split = segment_candidate.split(".")
                        original_class_split = segment_original.split(".")
                        if not is_subgroup_of_class_spec(candidate_class_split, original_class_split):
                            return False
                    else:
                        if segment_original != segment_candidate:
                            return False
            else:
                return False
        else:
            return False
        return True
    except ValueError:
        print("Value Error: Original: " + ''.join(original) + ", Candidato: " + ''.join(candidate))
        return False


def is_equivalent_rule_list(original, candidate_list):
    over_protective_rule = []
    for candidate in candidate_list:
        if original.split('#')[0] != candidate.split('#')[0] and \
                is_equivalent_rule(original.split('#')[0], candidate.split('#')[0]):
            over_protective_rule.append(candidate)
    return over_protective_rule


class Tester:

    @staticmethod
    def listSimilarityPercentage(comparing, reference, negativeRules, prnt=False, app=None, folder='results'):

        correctRules = []
        extraRules = []

        list1len = len(comparing)
        referenceLen = len(reference)

        falseNegative = []
        trueNegative = []
        for r in negativeRules:
            toCompare = r.split('#', 1)[0]
            if toCompare in reference:
                falseNegative.append(r)
            else:
                trueNegative.append(r)

        for elm1 in comparing:
            toCompare = elm1.split('#', 1)[0]
            if elm1 in reference:
                correctRules.append(elm1)
                reference.remove(elm1)
            elif toCompare in reference:
                correctRules.append(elm1)
                reference.remove(toCompare)
            else:
                extraRules.append(elm1)

        missingRules = reference

        missingDepRules = 0
        missingImportRules = 0
        missinAppSpecificRules = 0
        missingRulesOther = 0

        newCorrect = []
        if prnt:
            path = folder + "/" + app.getName()
            f = open(path + "/GeneratedVsExtracted_" + app.getName() + ".pro", "w")

            # Chequeamos como son las reglas que nos faltaron

            deps = app.getDependencies()
            imports = app.getAllImports()
            relatedImports = []
            for dep in deps:
                for im in imports:
                    if dep in im:
                        imAAgregar = im.split(".")[-1]
                        if imAAgregar == "*" or imAAgregar == "**":
                            imAAgregar = im.split(".")[-2]
                        if imAAgregar not in relatedImports:
                            relatedImports.append(imAAgregar)

            necessary_over_protected_rule_count = 0
            over_protected_rule_count = 0
            f.write('Missing Rules:\n')
            for elm4 in missingRules:
                over_protective_rule = is_equivalent_rule_list(elm4, extraRules)
                if over_protective_rule:
                    write_rule = elm4 + " # over protected by; \n"
                    for rule in over_protective_rule:
                        extraRules.remove(rule)
                        write_rule = write_rule + "\t\t# " + rule + "\n"
                        necessary_over_protected_rule_count += 1
                        over_protected_rule_count += 1
                    newCorrect.append(write_rule)
                    missingRules.remove(elm4)
                elif '## is app specific rule' in elm4:
                    missinAppSpecificRules += 1
                    f.write('\t' + elm4 + '\n')
                else:
                    seenDeps = False
                    for dep in deps:
                        if dep in elm4:
                            missingDepRules += 1
                            f.write('\t' + elm4 + ' # from dep ' + dep + '\n')
                            seenDeps = True
                            break
                    if not seenDeps:
                        seenImports = False
                        for im in relatedImports:
                            if im in elm4:
                                missingImportRules += 1
                                f.write('\t' + elm4 + ' # from import ' + im + '\n')
                                seenImports = True
                                break
                        if not seenImports:
                            missingRulesOther += 1
                            f.write('\t' + elm4 + '\n')
            over_protected_correct_rule_count = 0
            f.write('\nCorrectly Generated Rules:\n')
            for elm3 in correctRules:
                over_protective_rule = is_equivalent_rule_list(elm3, extraRules)
                if over_protective_rule:
                    over_protected_rule_count += 1
                    over_protected_correct_rule_count += 1
                    elm3 = elm3 + "# over protected by; \n"
                    for rule in over_protective_rule:
                        extraRules.remove(rule)
                        elm3 = elm3 + "\t\t# " + rule + "\n"
                f.write('\t' + elm3 + '\n')

            for elm6 in newCorrect:
                f.write('\t' + elm6 + '\n')

            f.write('\nFalse Negative Rules:\n')
            for elm5 in falseNegative:
                f.write('\t' + elm5 + '\n')

            f.write('\nOverly Generated Rules:\n')
            extraRules.sort()
            for elm5 in extraRules:
                over_protective_rule = is_equivalent_rule_list(elm5, extraRules)
                if over_protective_rule:
                    for rule in over_protective_rule:
                        over_protected_rule_count += 1
                f.write('\t' + elm5 + '\n')
            f.close()

        countCorrect = len(correctRules) + len(newCorrect)
        percentageIn = (countCorrect / referenceLen) * 100
        if list1len > 0:
            percentageExtra = (len(extraRules) / list1len) * 100
        else:
            percentageExtra = 100
        countMissing = len(missingRules)

        percentageRemainding = 0
        perMissingDepRules = 0
        perMissingImportRules = 0
        perMissingAppSpecificRules = 0
        perMissingRulesOther = 0
        perOverProtectedRules = 0
        necessary_perOverProtectedRules = 0
        perOverProtectedCRules = 0

        accuracy = (countCorrect + len(trueNegative))/\
                   (countCorrect + len(trueNegative) + len(extraRules) + len(falseNegative))
        precision = countCorrect/(countCorrect + len(extraRules))
        if countCorrect + len(falseNegative) == 0.0:
            recall = 0
        else:
            recall = countCorrect/(countCorrect + len(falseNegative))
        if recall == 0.0 and precision == 0.0:
            f1score = 0
        else:
            f1score = (2*(recall*precision))/(recall + precision)

        if countCorrect != 0:
            perOverProtectedCRules = (over_protected_correct_rule_count/countCorrect)*100
            necessary_perOverProtectedRules = (necessary_over_protected_rule_count/countCorrect)*100
            perOverProtectedRules = (over_protected_rule_count/list1len)*100

        if countMissing != 0:
            percentageRemainding = (countMissing / referenceLen) * 100
            perMissingDepRules = (missingDepRules / countMissing)*100
            perMissingImportRules = (missingImportRules / countMissing) * 100
            perMissingAppSpecificRules = (missinAppSpecificRules / countMissing) * 100
            perMissingRulesOther = (missingRulesOther / countMissing)*100
        return {"correct": percentageIn, "extra": percentageExtra, "missing": percentageRemainding,
                "missingDepRules": perMissingDepRules, "missingImportRules": perMissingImportRules,
                "missingAppSpecificRules": perMissingAppSpecificRules, "missingRulesOther": perMissingRulesOther,
                "overProtectedRules": perOverProtectedRules, 'perOverProtectedCRules':perOverProtectedCRules,
                'necessary_perOverProtectedRules': necessary_perOverProtectedRules,
                'precision': precision, 'accuracy': accuracy, 'recall': recall, 'f1score': f1score}

    @staticmethod
    def ruleGeneratingTestTemplate(methodToTest, appsToTest, timesToAverage=50,  percentage=5, folder='results',
                                   especificacionesExp="perc 5%, imports, index", checkApk=False):
        print("\n")

        correctPrTot = 0
        extraPrTot = 0
        missingPrTot = 0

        missingDepTot = 0
        missingImportTot = 0
        missingAppSpecificTot = 0
        missingOthersTot = 0

        precisionTot = 0
        accuracyTot = 0
        recallTot = 0
        f1scoreTot = 0

        overProtectedTot = 0
        overProtectedCTot = 0
        NoverProtectedTot = 0
        completelyCorrectRules = 0

        f = open(folder + "/percentage-comp-test.csv", "w")
        f.write("Percentage, Correct, Extra, Remainder\n")

        with alive_bar(timesToAverage) as bar:
            for i in range(0, timesToAverage):

                appTested = appsToTest[i]
                if checkApk:
                    show = 'Unpacking APK for Clean Up: ' + appTested.getName()
                    bar.text(show)
                    appTested.unpackApk(bar, show)

                bar.text('Generating Rules for ' + appTested.getName() + '...' + str(percentage) + '% ')

                rulesGenerated, negativeRules = methodToTest(appTested, percentage, True, checkApk=checkApk)

                rulesExtracted = appTested.getRules()

                bar.text('Comparing Rules ' + appTested.getName() + str(percentage) + '% ')
                similarities = Tester.listSimilarityPercentage(rulesGenerated, rulesExtracted,
                                                               negativeRules, True, appTested, folder)

                correctPr = similarities["correct"]
                extraPr = similarities["extra"]
                missingPr = similarities["missing"]
                missingDepPr = similarities["missingDepRules"]
                missingImportPr = similarities["missingImportRules"]
                missingAppSpecificPr = similarities["missingAppSpecificRules"]
                missingRulesOtherPr = similarities["missingRulesOther"]
                overProtectedRulesPr = similarities["overProtectedRules"]
                NoverProtectedRulesPr = similarities["necessary_perOverProtectedRules"]
                perOverProtectedCRules = similarities["perOverProtectedCRules"]

                precision = similarities["precision"]
                accuracy = similarities["accuracy"]
                recall = similarities["recall"]
                f1score = similarities["f1score"]

                correct = str(round(correctPr, 2))
                extra = str(round(extraPr, 2))
                missing = str(round(missingPr, 2))
                missingDep = str(round(missingDepPr, 2))
                missingImport = str(round(missingImportPr, 2))
                missingAppSpecific = str(round(missingAppSpecificPr, 2))
                missingOther = str(round(missingRulesOtherPr, 2))
                overProtectedRules = str(round(overProtectedRulesPr, 2))
                NoverProtectedRules = str(round(NoverProtectedRulesPr, 2))
                overProtectedCRules = str(round(perOverProtectedCRules, 2))

                if round(correctPr, 2) == 100.0:
                    completelyCorrectRules += 1

                f.write(str(i / 10) + ", " + correct + ", " + extra + ", " + missing + "\n")
                print("\n********************\n" + appTested.getName() + "\n")
                print("Correct Avg: " + correct)
                print("OverProtected Rules: " + overProtectedRules)
                print("OverProtected Correct Rules: " + overProtectedCRules)
                print("Necessary OverProtected Rules: " + NoverProtectedRules)
                print("Missing Avg: " + missing)
                print("Extra Avg: " + extra)
                print("---------Data Science Pointers---------")
                print("Precision: " + str(round(precision, 2)))
                print("Accuracy: " + str(round(accuracy, 2)))
                print("recall: " + str(round(recall, 2)))
                print("F1 Score: " + str(round(f1score, 2)))
                print("----------Missing Rules Type-----------")
                print("Missing Dep Rules: " + missingDep)
                print("Missing Import Rules: " + missingImport)
                print("Missing App Specific Rules: " + missingAppSpecific)
                print("Missing Other Rules: " + missingOther)

                correctPrTot = correctPrTot + correctPr
                extraPrTot = extraPrTot + extraPr
                missingPrTot = missingPrTot + missingPr

                missingDepTot += missingDepPr
                missingImportTot += missingImportPr
                missingAppSpecificTot += missingAppSpecificPr
                missingOthersTot += missingRulesOtherPr

                recallTot += recall
                precisionTot += precision
                accuracyTot += accuracy
                f1scoreTot += f1score

                overProtectedTot += overProtectedRulesPr
                overProtectedCTot += perOverProtectedCRules
                NoverProtectedTot += NoverProtectedRulesPr

                bar()

        f.close()
        print("********************\nExperimento:", especificacionesExp, "\n********************")
        print("Correct Avg: " + str(round(correctPrTot / timesToAverage, 2)))
        print("OverProtected Rules: " + str(round(overProtectedTot / timesToAverage, 2)))
        print("OverProtected Correct Rules: " + str(round(overProtectedCTot / timesToAverage, 2)))
        print("Necessary OverProtected Rules: " + str(round(NoverProtectedTot / timesToAverage, 2)))
        print("Missing Avg: " + str(round(missingPrTot / timesToAverage, 2)))
        print("Extra Avg: " + str(round(extraPrTot / timesToAverage, 2)))
        print("Completely Correct Rules: " + str(round(completelyCorrectRules / timesToAverage * 100, 2)))
        print("---------Data Science Pointers---------")
        print("Precision: " + str(round(precisionTot/timesToAverage, 2)))
        print("Accuracy: " + str(round(accuracyTot/timesToAverage, 2)))
        print("recall: " + str(round(recallTot/timesToAverage, 2)))
        print("F1 Score: " + str(round(f1scoreTot/timesToAverage, 2)))
        print("-----------Missing Rules Type-----------")
        print("Missing Dep Rules: " + str(round(missingDepTot / timesToAverage, 2)))
        print("Missing Import Rules: " + str(round(missingImportTot / timesToAverage, 2)))
        print("Missing App Specific Rules: " + str(round(missingAppSpecificTot / timesToAverage, 2)))
        print("Missing Other Rules: " + str(round(missingOthersTot / timesToAverage, 2)))

    @staticmethod
    def ruleGeneratingTestDB(db: DBConnect=DBConnect('root', 'Juan.suaz0'), specificAppsToTest=[], timesToAverage=50,
                             percentage=5, folder='resultsDB', checkApk=False):

        print("\n")

        dbAnalyser = DataBaseAnalyser(db)

        method = dbAnalyser.rulesForAllDepsExcludingApp

        f = open("results/percentage-comp-test.csv", "w")
        f.write("Percentage, Correct, Extra, Remainder\n")
        if specificAppsToTest:
            appsToTest = []
            with alive_bar(timesToAverage) as bar:
                bar.text('Retrieving Apps To Test and Generating App Objects: ')
                for app in specificAppsToTest:
                    bar.text('Retrieving Apps To Test and Generating App Objects: ' + app.rsplit('/', 1)[1])
                    appsToTest.append(App(app))
                    bar()
            Tester.ruleGeneratingTestTemplate(method, appsToTest, timesToAverage, percentage, folder, checkApk=checkApk)
        else:
            appsToTest = []
            with alive_bar(timesToAverage) as bar:
                bar.text('Retrieving Apps To Test and Generating App Objects: ')
                pathsToTest = db.getAppsToTest(timesToAverage)

                for path in pathsToTest:
                    bar.text('Retrieving Apps To Test and Generating App Objects: ' + path.rsplit('/', 1)[1])
                    appsToTest.append(App(path))
                    bar()
            Tester.ruleGeneratingTestTemplate(method, appsToTest, timesToAverage, percentage, folder, checkApk=checkApk)

            db.close()

    @staticmethod
    def ruleGeneratingTestObject(pathToRepo='/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps',
                                 timesToAverage=50, percentage=5, folder='results', checkApk=False):
        repo = FDroid(pathToRepo)
        print("\n")

        analyser = FDroidAnalyser(repo)
        method = analyser.rulesForAllDepsExcludingApp
        # especificacionesExp = "perc " + str(percentage) + "%, imports, index"

        appsToTest = []
        pathsForComparison = []

        with alive_bar(timesToAverage) as bar:
            for i in range(0, timesToAverage):

                bar.text(' Selecting Apps to Test...')
                while len(appsToTest) < timesToAverage:
                    app = repo.randomObfuscatedDontWarn()

                    if len(app.analyser.rulesForDeps()) > 1 and len(
                            app.getDependencies()) > 1 and app not in appsToTest:
                        appsToTest.append(app)
                        pathsForComparison.append(app.getPath())
                bar()
        Tester.ruleGeneratingTestTemplate(method, appsToTest, timesToAverage, percentage, folder, checkApk)
        return pathsForComparison

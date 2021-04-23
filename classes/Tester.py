import sys
from alive_progress import alive_bar
from classes.FDroidClass import FDroid
from classes.Aplication import App
from classes.DBConnect import DBConnect
from analysis.fdroidAnalyser import FDroidAnalyser, DataBaseAnalyser

sys.path.insert(1, '/Volumes/WanShiTong/Archive/UChile/Título/work/Src')


class Tester:

    def __init__(self):
        pass

    @staticmethod
    def listSimilarityPercentage(comparing, reference, prnt=False, app=None, folder='results'):
        correctRules = []
        extraRules = []
        missingRules = []

        list1len = len(comparing)
        list2len = len(reference)

        for elm1 in comparing:
            if elm1 in reference:
                correctRules.append(elm1)
            else:
                extraRules.append(elm1)

        for elm2 in reference:
            if elm2 not in correctRules:
                missingRules.append(elm2)

        if prnt:
            path = folder + "/" + app.getName()
            f = open(path + "/GeneratedVsExtracted_" + app.getName() + ".pro", "w")

            f.write('Correctly Generated Rules:\n')
            for elm3 in correctRules:
                f.write('\t' + elm3 + '\n')

            f.write('\nMissing Rules:\n')
            for elm4 in missingRules:
                f.write('\t' + elm4 + '\n')

            f.write('\nOverly Generated Rules:\n')
            for elm5 in extraRules:
                f.write('\t' + elm5 + '\n')

        countCorrect = len(correctRules)

        percentageIn = (countCorrect / list2len) * 100

        if list1len > 0:
            percentageExtra = ((list1len - countCorrect) / list1len) * 100
        else:
            percentageExtra = 100
        percentageRemainding = ((list2len - countCorrect) / list2len) * 100

        return {"correct": percentageIn, "extra": percentageExtra, "remainding": percentageRemainding}

    @staticmethod
    def ruleGeneratingTestTemplate(methodToTest, appsToTest, timesToAverage=50,
                                   percentage=5, folder='results', especificacionesExp="perc 5%, imports, index"):
        print("\n")

        correctPrTot = 0
        extraPrTot = 0
        missingPrTot = 0

        f = open(folder + "/percentage-comp-test.csv", "w")
        f.write("Percentage, Correct, Extra, Remainder\n")

        with alive_bar(timesToAverage) as bar:
            for i in range(0, timesToAverage):

                appTested = appsToTest[i]

                bar.text('Generating Rules for ' + appTested.getName() + '...' + str(i) + '% ')

                rulesGenerated = methodToTest(appTested, percentage, True)

                rulesExtracted = appTested.getRules()

                similarities = []

                bar.text('Comparing Rules' + str(percentage) + '% ')

                extracted = rulesExtracted
                generated = rulesGenerated

                sim = Tester.listSimilarityPercentage(generated, extracted, True, appTested, folder)
                similarities.append(sim)

                correctPr = 0
                extraPr = 0
                missingPr = 0

                for elm in similarities:
                    correctPr += (elm["correct"])
                    extraPr += (elm["extra"])
                    missingPr += (elm["remainding"])

                correct = str(round(correctPr, 2))
                extra = str(round(extraPr, 2))
                missing = str(round(missingPr, 2))

                f.write(str(i / 10) + ", " + correct + ", " + extra + ", " + missing + "\n")
                print("\n********************\n" + appTested.getName() + "\n")
                print("Correct Avg: " + correct)
                print("Missing Avg: " + missing)
                print("Extra Avg: " + extra)

                correctPrTot = correctPrTot + correctPr
                extraPrTot = extraPrTot + extraPr
                missingPrTot = missingPrTot + missingPr

                bar()

        f.close()
        print("********************\nExperimento:", especificacionesExp, "\n********************")
        print("Correct Avg: " + str(round(correctPrTot / timesToAverage, 2)))
        print("Missing Avg: " + str(round(missingPrTot / timesToAverage, 2)))
        print("Extra Avg: " + str(round(extraPrTot / timesToAverage, 2)))

    @staticmethod
    def ruleGeneratingTestDB(pathsForComparison, db: DBConnect=DBConnect('root', 'Juan.suaz0'), timesToAverage=50, percentage=5, folder='resultsDB'):

        print("\n")

        dbAnalyser = DataBaseAnalyser(db)

        method = dbAnalyser.rulesForAllDepsExcludingApp

        f = open("results/percentage-comp-test.csv", "w")
        f.write("Percentage, Correct, Extra, Remainder\n")

        appsToTest = []
        with alive_bar(1) as bar:
            pathsToTest = db.getAppsToTest(timesToAverage)

            for path in pathsForComparison:
                appsToTest.append(App(path))
            bar()
        Tester.ruleGeneratingTestTemplate(method, appsToTest, timesToAverage, percentage, folder)

        db.close()

    @staticmethod
    def ruleGeneratingTestObject(pathToRepo='/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps', timesToAverage=50, percentage=5, folder='results'):
        repo = FDroid(pathToRepo, True)
        print("\n")

        analyser = FDroidAnalyser(repo)
        method = analyser.rulesForAllDepsExcludingApp
        especificacionesExp = "perc " + str(percentage) + "%, imports, index"

        appsToTest = []
        pathsForComparison = []

        with alive_bar(timesToAverage) as bar:
            for i in range(0, timesToAverage):

                bar.text(' Selecting Apps to Test...')
                while len(appsToTest) < timesToAverage:
                    app = repo.randomObfuscatedDontWarn()

                    if len(app.rulesForDeps()) > 1 and len(
                            app.getDependencies()) > 1 and app not in appsToTest:
                        appsToTest.append(app)
                        pathsForComparison.append(app.getPath())
                bar()
        Tester.ruleGeneratingTestTemplate(method, appsToTest, timesToAverage, percentage, folder)
        return pathsForComparison

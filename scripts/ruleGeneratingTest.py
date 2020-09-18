if __name__ == '__main__':
    from classes.FDroidClass import FDroid
    from analysis.fdroidAnalyser import FDroidAnalyser, AppAnalyser

    def listSimilarityPercentage(list1, list2):

        countInList = 0

        for elm in list1:
            if elm in list2: countInList +=1

        percentageIn = (countInList/len(list2))*100

        if len(list1) > 0:
            percentageExtra = ((len(list1)-countInList)/len(list1))*100
        else:
            percentageExtra = 100
        percentageRemainding = ((len(list2)-countInList)/len(list2))*100

        return {"correct": percentageIn, "extra": percentageExtra, "remainding": percentageRemainding}

    path = "/Volumes/Box1/JPS/intTrabajoTitulo/work/obfApps"
    repo = FDroid(path)

    analyser = FDroidAnalyser(repo)

    appsToTest = []

    while len(appsToTest) < 50:
        app = repo.randomObfuscatedDontWarn()

        if app not in appsToTest and len(AppAnalyser(app).rulesForDeps()) > 1 and len(app.getDependencies()) > 1:
            appsToTest.append(app)


    rulesGenerated = analyser.rulesForAllDepsList(appsToTest)

    rulesExtracted = []

    for app in appsToTest:
        rulesExtracted.append(AppAnalyser(app).rulesForDeps())

    similarities = []

    for i in range(len(rulesGenerated)):
        extracted = rulesExtracted[i]
        generated = rulesGenerated[i]
        sim = listSimilarityPercentage(generated, extracted)
        similarities.append(sim)
        print(str(sim) + "\n")
        print("********************\n********************")

    correctPr = 0
    extraPr = 0
    remainderPr = 0

    for elm in similarities:
        correctPr += (elm["correct"])
        extraPr += (elm["extra"])
        remainderPr += (elm["remainding"])

    print("Correct Avg: " + str(correctPr/100))
    print("Extra Avg: " + str(extraPr / 100))
    print("Remainder Avg: " + str(remainderPr / 100))

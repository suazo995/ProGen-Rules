if __name__ == '__main__':
    import sys
    sys.path.insert(1, '/Volumes/Box1/JPS/intTrabajoTitulo/work/Src')

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

    path = "/Volumes/Box1/JPS/intTrabajoTitulo/work/" + sys.argv[2]
    repo = FDroid(path)
    print("\n")

    analyser = FDroidAnalyser(repo)

    correctPrTot = 0
    extraPrTot = 0
    remainderPrTot = 0

    for i in range(10):

        appsToTest = []

        Num = int(sys.argv[1])

        while len(appsToTest) < Num:
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
            #print(str(sim) + "\n")
            #print("********************\n********************")

        correctPr = 0
        extraPr = 0
        remainderPr = 0

        for elm in similarities:
            correctPr += (elm["correct"])
            extraPr += (elm["extra"])
            remainderPr += (elm["remainding"])

        print("Correct Avg: " + str(correctPr/Num))
        print("Extra Avg: " + str(extraPr / Num))
        print("Remainder Avg: " + str(remainderPr / Num))
        print("\n********************\n")

        correctPrTot = correctPrTot + (correctPr/Num)
        extraPrTot = extraPrTot + (extraPr / Num)
        remainderPrTot = remainderPrTot + (remainderPr / Num)

    print("********************\n********************\n")
    print("Correct Avg: " + str(correctPrTot / 10))
    print("Extra Avg: " + str(extraPrTot / 10))
    print("Remainder Avg: " + str(remainderPrTot / 10))
    print("\n********************\n********************\n")

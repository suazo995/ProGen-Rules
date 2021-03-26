if __name__ == '__main__':
    import sys
    if sys.argv[1]=="-h" or sys.argv[1]=="--h" or sys.argv[1]=="--help":
        print("Argumentos del Comando: <Cantidad de Apps a Testear> <Carpeta de la Repo> <Nº de Bloques de Porcentajes a Comparar>")
    else:
        sys.path.insert(1, '/Volumes/WanShiTong/Archive/UChile/Título/work/Src')

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


        path = '/Volumes/WanShiTong/Archive/UChile/Título/work/' + sys.argv[2]
        repo = FDroid(path)
        analyser = FDroidAnalyser(repo)
        print("\n")

        f = open("../../results/testPorcentajes.csv", "w")
        f.write("Porcentaje de Presencia, Correctas, Sobrantes, Faltantes\n")

        blocksPorcentages = int(sys.argv[3])

        for i in range(blocksPorcentages):
            percentage = (i+1)*(100/blocksPorcentages)

            correctPrTot = 0
            extraPrTot = 0
            remainderPrTot = 0

            for k in range(10):

                appsToTest = []

                Num = int(sys.argv[1])

                while len(appsToTest) < Num:
                    app = repo.randomObfuscatedDontWarn()
                    appAnalyser = AppAnalyser(app)

                    if app not in appsToTest and len(appAnalyser.rulesForDeps()) > 1 and len(app.getDependencies()) > 1:
                        appsToTest.append(app)


                rulesGenerated = analyser.rulesForAllDepsList(appsToTest, percentage)

                rulesExtracted = []

                for app in appsToTest:
                    rulesExtracted.append(app.getRules())

                similarities = []

                for j in range(len(rulesGenerated)):
                    extracted = rulesExtracted[j]
                    generated = rulesGenerated[j]
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
            f.write(str(percentage) + "%, " + str(correctPrTot / 10) + ", " + str(extraPrTot / 10) + ", " +
                    str(remainderPrTot / 10) + "\n")

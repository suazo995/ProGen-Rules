if __name__ == '__main__':
    from classes.FDroidClass import FDroid
    from analysis.fdroidAnalyser import FDroidAnalyser

    path = "/Volumes/Box1/JPS/intTrabajoTitulo/work/obfApps"
    repo = FDroid(path)

    print("Apps ofuscadas: ", repo.numObfuscatedApps())
    print("Apps no ofuscadas: ", repo.numUnObfuscatedApps())

    analyser = FDroidAnalyser(repo)

    analyser.numberOfRules()
    analyser.obfVsSinObf()
    analyser.obfWithDontObf()
    analyser.dependenciesHistogram()
    analyser.depRuleHistogram()
    analyser.sameDepNumDeps()
    analyser.mostUsedDeps()
    analyser.mostRulesDeps()
    # analyser.appsThatUseDep("okhttp")
    # analyser.appsThatUseDep("glide")
    # analyser.appsThatUseDep("retrofit")
    # analyser.appsThatUseDep("butterknife")
    # analyser.rulesForDepExcludingApp("butterknife", "AuroraDroid", True)

if __name__ == '__main__':
    import sys

    # insert at 1, 0 is the script path (or '' in REPL)
    sys.path.insert(1, '/Volumes/Box1/JPS/intTrabajoTitulo/work/Src')

    from classes.FDroidClass import FDroid
    from analysis.fdroidAnalyser import FDroidAnalyser

    path = "/Volumes/Box1/JPS/intTrabajoTitulo/work/miniSet"
    repo = FDroid(path)

    print("Apps ofuscadas: ", repo.numObfuscatedApps())
    print("Apps no ofuscadas: ", repo.numUnObfuscatedApps())


    # analyser = FDroidAnalyser(repo)
    #
    # analyser.numberOfRules()
    # analyser.obfVsSinObf()
    # analyser.obfWithDontObf()
    # analyser.dependenciesHistogram()
    # analyser.depRuleHistogram()
    # analyser.sameDepNumDeps()
    # analyser.mostUsedDeps()
    # analyser.mostRulesDeps()
    # # analyser.appsThatUseDep("okhttp")
    # # analyser.appsThatUseDep("glide")
    # # analyser.appsThatUseDep("retrofit")
    # # analyser.appsThatUseDep("butterknife")
    # # analyser.rulesForDepExcludingApp("butterknife", "AuroraDroid", True)

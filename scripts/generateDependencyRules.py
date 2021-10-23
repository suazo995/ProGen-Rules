#!/usr/bin/python3
import sys, getopt, os

from alive_progress import alive_bar
from classes.Aplication import App
from classes.DBConnect import DBConnect
from analysis.DataBaseAnalyser import DataBaseAnalyser


def generateDependencyRules(specificAppToTest, db: DBConnect=DBConnect('root', 'Juan.suaz0'), percentage=5,
                            checkApk=False, outdir=None, verbose=None):
    if checkApk:
        barn=3
    else:
        barn=2
    print("\n")
    with alive_bar(barn) as bar:
        dbAnalyser = DataBaseAnalyser(db)

        method = dbAnalyser.rulesForAllDepsExcludingApp
        if verbose:
            bar.text('Generating Application Object')
        app = App(specificAppToTest)
        bar()

        if checkApk:
            show = 'Unpacking APK for Clean Up: ' + app.getName()
            if verbose:
                bar.text(show)
            app.unpackApk(bar, show, verbose)
            bar()

        if verbose:
            bar.text('Generating Rules for ' + app.getName())

        rulesGenerated, negativeRules = method(app, percentage, True, checkApk=checkApk)
        bar()

        sortedRules = sorted(rulesGenerated)

        if outdir:
            f_keep = open(outdir + "/GeneratedKeepRules.pro", "w")
            f_dont = open(outdir + "/GeneratedDontWarnRules.pro", "w")

        else:
            f_keep = open(app.getPath() + "/GeneratedKeepRules.pro", "w")
            f_dont = open(app.getPath() + "/GeneratedDontWarnRules.pro", "w")

        for rule in sortedRules:
            if 'keep' in rule:
                f_keep.write('-'+rule+'\n')
            else:
                f_dont.write('-'+rule+'\n')

def main(argv):
    outputdir = None
    appdir = '---'
    verbose = False
    try:
        opts, args = getopt.getopt(argv,"hvd:p:",["dir=","path="])
    except getopt.GetoptError:
        print('generateDependencyRules.py -p <application-project-path> <options>\n\n'
              'options:     -v: Makes command verbose.\n'
              '             -d,--dir: Directory in which to write the rule files.\n'
              '             -h: Displays this prompt.')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('generateDependencyRules.py -p <application-project-path> <options>\n\n'
                  'options:     -v: Makes command verbose.\n'
                  '             -d,--dir: Directory in which to write the rule files.\n'
                  '             -h: Displays this prompt.')
            sys.exit()
        elif opt in ("-v"):
            verbose = True
        elif opt in ("-d", "--dir"):
            outputdir = arg
        elif opt in ("-p", "--path"):
            appdir = arg

    generateDependencyRules(str(appdir), checkApk=True, outdir=outputdir, verbose=verbose)


if __name__ == "__main__":
   main(sys.argv[1:])

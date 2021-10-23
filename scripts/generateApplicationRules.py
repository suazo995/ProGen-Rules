#!/usr/bin/python3
import sys, getopt, os

from alive_progress import alive_bar
from classes.Aplication import App
from classes.DBConnect import DBConnect
from analysis.DataBaseAnalyser import DataBaseAnalyser


def generateApplicationRules(specificAppToTest, noRes, noJNI, noData, db: DBConnect=DBConnect('root', 'Juan.suaz0'),
                             checkApk=False, outdir=None, verbose=False):
    barn=5
    print("\n")
    with alive_bar(barn) as bar:
        dbAnalyser = DataBaseAnalyser(db)

        method = dbAnalyser.rulesForAllDepsExcludingApp
        if verbose: bar.text('Generating Application Object')
        app = App(specificAppToTest)
        bar()

        if verbose: bar.text('Generating Rules for ' + app.getName())

        data_class_rules, unObfCases = app.getRulesForDataClasses()
        apk_rules, unObfCases = app.getRulesForResourceLoadingFromAPK()
        jni_rules, unObfCases = app.getRulesForClassesLoadedFromNativeSide()
        bar()

        if outdir:
            f_keep = open(outdir + "/GeneratedApplicationRules.pro", "w")
        else:
            f_keep = open(app.getPath() + "/GeneratedApplicationRules.pro", "w")

        if verbose: bar.text('Writing Rules for ' + app.getName())
        write_Title_data = True
        if data_class_rules and not noData:
            for rule in data_class_rules:
                if write_Title_data:
                    f_keep.write('#Rules For Suspected Data Classes:'+'\n'+'\n')
                    write_Title_data = False
                f_keep.write('-' + rule + '\n')

            f_keep.write("\n")
        bar()

        write_Title_apk = True
        if apk_rules and not noRes:
            for rule2 in apk_rules:
                if write_Title_apk:
                    f_keep.write('#Rules For Suspected APK Loading:'+'\n'+'\n')
                    write_Title_apk = False
                f_keep.write('-' + rule2 + '\n')

            f_keep.write("\n")
        bar()

        write_Title_jni = True
        if jni_rules and not noJNI:
            for rule3 in jni_rules:
                if write_Title_jni:
                    f_keep.write('#Rules For Suspected JNI Calls:'+'\n'+'\n')
                    write_Title_jni = False
                f_keep.write('-' + rule3 + '\n')
        bar()

def main(argv):
    outputdir = ''
    appdir = ''
    noRes = False
    noJNI = False
    noData = False
    verbose = False
    try:
        opts, args = getopt.getopt(argv,"hvd:p:",["dir=","path=", "noRes", "noJNI", "noData"])
    except getopt.GetoptError:
        print('generateDependencyRules.py -p <application-project-path> <options>\n\n'
              'options:     -v: Makes command verbose.\n'
              '             -d,--dir: Directory in which to write the rule files.\n'
              '             --noRes: Disables rule generation for APK resource loading.\n'
              '             --noJNI: Disables rule generation for JNI calls.\n'
              '             --noData: Disables rule generation for Data Classes.\n'
              '             -h: Displays this prompt.')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('generateDependencyRules.py -p <application-project-path> <options>\n\n'
                  'options:     -v: Makes command verbose.\n'
                  '             -d,--dir: Directory in which to write the rule files.\n'
                  '             --noRes: Disables rule generation for APK resource loading.\n'
                  '             --noJNI: Disables rule generation for JNI calls.\n'
                  '             --noData: Disables rule generation for Data Classes.\n'
                  '             -h: Displays this prompt.')
            sys.exit()
        elif opt in ("-v"):
            verbose = True
        elif opt in ("-d", "--dir"):
            outputdir = arg
        elif opt in ("-p", "--path"):
            appdir = arg
        elif opt in ("--noRes"):
            noRes = True
        elif opt in ("--noJNI"):
            noJNI = True
        elif opt in ("--noData"):
            noData = True

    generateApplicationRules(str(appdir), noRes, noJNI, noData, checkApk=True, outdir=outputdir, verbose=verbose)


if __name__ == "__main__":
   main(sys.argv[1:])

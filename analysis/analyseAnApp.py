"""
Script para analisar una app.
"""

import sys

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/Volumes/Box1/JPS/intTrabajoTitulo/work/Src')

from classes.AppClass import App
from analysis.fdroidAnalyser import AppAnalyser
from pprint import pprint

path = "/Volumes/Box1/JPS/intTrabajoTitulo/work/fdroidapps/GameDealz/"

app = App(path)
pprint(app.dontObfuscateRule)
pprint(app.dontObfuscateFiles)
print('')
for pg in app.proguardRuleFiles:
    pprint(pg.name)
    pprint(pg.rules.rules)

print('')

analyser = AppAnalyser(app)
analyser.rulesForDeps()

pprint(app.getAllImports())

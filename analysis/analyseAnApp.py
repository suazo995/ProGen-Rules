"""
Script para analisar una app.
"""

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

from classes.FDroidClass import FDroid

path = "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps"
repo = FDroid(path)

for app in repo.apps:
    if app.getPgFiles() and not app.getRules() and not app.getDontObfuscateRule():
        print(app.getName())

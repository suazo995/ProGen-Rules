import os
rootdir=('/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/Readrops')
for folder, dirs, files in os.walk(rootdir):
        for file in files:
            fullpath = os.path.join(folder, file)
            try:
                with open(fullpath, 'r') as f:
                    for line in f:
                        if "xmlpull" in line:
                            print(fullpath)
            except:
                print('error en ', fullpath)
import os
rootdir = '/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/Conversations'
number = 0
for folder, dirs, files in os.walk(rootdir):
        for file in files:
            fullpath = os.path.join(folder, file)
            if fullpath.rsplit('.', 1)[-1]=="java":
                try:
                    with open(fullpath, 'r') as f:
                        for line in f:
                            if ".getResourceAsStream(" in line or ".getResource(" in line:
                                print(fullpath.split("obfApps/", 1)[1], line)
                                number += 1
                                break
                except:
                    pass
print(number)
import os
import re

rootdir = '/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/Xabber'
number = 0
for folder, dirs, files in os.walk(rootdir):
        for file in files:
            fullpath = os.path.join(folder, file)
            extension = fullpath.rsplit('.', 1)[-1]
            if extension == "java":
                try:
                    with open(fullpath, 'r') as f:
                        for line in f:
                            if re.findall(".*(\.getResource(AsStream)?\().*", line):
                                print(fullpath.split("obfApps/", 1)[1], line)
                                number += 1
                                break

                except:
                    pass
print(number)

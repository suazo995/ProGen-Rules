import os
import re

rootdir = '/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps'
number = 0
for folder, dirs, files in os.walk(rootdir):
        for file in files:
            fullpath = os.path.join(folder, file)
            if fullpath.rsplit('.', 1)[-1] == "java" or fullpath.rsplit('.', 1)[-1] == "kt":
                try:
                    with open(fullpath, 'r') as f:
                        for line in f:
                            if re.findall(".*\.getResource(AsStream)?\(.*", line):
                                print(fullpath.split("obfApps/", 1)[1], line)
                                number += 1

                except:
                    pass
print(number)
import re


def isolate_class_references(rule):
    ret = []

    class_specification_rules = ['keep', 'keepclassmembers', 'keepclasseswithmembers', 'keepnames',
                                 'keepclassmembernames', 'keepclasseswithmembernames', 'dontwarn', 'dontnote']
    ruleType = []
    afterBracket = ''
    if " extends " in rule or " implements " in rule:
        classAndExtended = rule.split(' extends ')
        if len(classAndExtended) == 1:
            classAndExtended = rule.split(' implements ')
        if '@' in classAndExtended[1]:
            classBeingExtended = classAndExtended[1].split(' ', 2)[1]
        else:
            classBeingExtended = classAndExtended[1].split(' ', 1)[0]
        extendingClass = classAndExtended[0].rsplit(' ', 1)[-1]
        ret.extend([extendingClass, classBeingExtended])
    elif rule.split(' ', 1)[0] in class_specification_rules:
        if ' {' in rule:
            aux = rule.split(' {', 1)
        else:
            aux = rule.split('{', 1)
        if len(aux) > 1:
            afterBracket = '{' + aux[1]
        classLocationReference = aux[0].rsplit(' ', 1)

        if len(classLocationReference) < 2:
            return []
        rulType = classLocationReference[0] + ' '
        classLocationReference = classLocationReference[1]


        if ',' in classLocationReference:
            classLocationReference = classLocationReference.split(',')
            for clsref in classLocationReference:
                rulType = re.sub('!', '', rulType)
                if '!' in clsref:
                    clsref = re.sub('!', '', clsref)
                    rulType = rulType + '!'
                ret.append(clsref)
                ruleType.append(rulType)
        else:
            classLocationReference = re.sub('!', '', classLocationReference)
            ret.append(classLocationReference)

    retLen = len(ret)

    annotations = re.findall('@(.*?) ', rule)
    if annotations:
        for ann in annotations:
            ret.append(ann)

    return ret, retLen, ruleType, afterBracket


class ProGuardAnalyser:

    @staticmethod
    def findFileRules(path: str, app):

        rulesToFilter = ['dontskipnonpubliclibraryclasses', 'skipnonpubliclibraryclasses',
                         'forceprocessing', 'dontshrink', 'printusage', 'whyareyoukeeping', 'dontoptimize',
                         'optimizations', 'optimizationpasses', 'assumenosideeffects', 'assumenoexternalsideeffects',
                         'assumenoescapingparameters', 'assumenoexternalreturnvalues', 'assumevalues',
                         'allowaccessmodification', 'mergeinterfacesaggressively', 'printmapping', 'applymapping',
                         'obfuscationdictionary', 'classobfuscationdictionary', 'packageobfuscationdictionary',
                         'overloadaggressively', 'useuniqueclassmembernames', 'dontusemixedcaseclassnames',
                         'flattenpackagehierarchy', 'repackageclasses', 'dontpreverify', 'microedition', 'verbose',
                         'ignorewarnings', 'printconfiguration', 'dump', 'addconfigurationdebugging']
        try:
            with open(path, 'r') as file:
                ret = []
                opened_rule = re.sub(r'(?m)^\s*#.*\n?', '', file.read())
                opened_rule = ' '.join(opened_rule.split())
                opened_rule = re.split("^-| -", opened_rule)[1:]
                # opened_rule = opened_rule.split("-")[1:]
                pattern = re.compile('[^a-zA-Z0-9_*.,;<>(){}@/!$ -]+')
                if opened_rule:
                    for rule in opened_rule:
                        rule = rule.split('#', 1)[0]

                        rule = re.sub(', ', ',', rule)
                        if "dontobfuscate" in rule:
                            app.dontObfuscateRule = True
                            app.dontObfuscateFiles.append(path)
                        elif "include " in rule:
                            fileToInclude = rule.split()[1]
                            pathToInclude = path.rsplit('/', 1)[0] + '/' + fileToInclude
                            app.appendPgFile(pathToInclude)
                        elif rule.split()[0] not in rulesToFilter:
                            rule = pattern.sub('', rule.replace("\\n", "").replace("\\r", "")).rstrip()

                            if rule == "dontwarn":
                                continue

                            clssAndLen = isolate_class_references(rule)
                            classSpecification = clssAndLen[0]
                            lenClassSpec = clssAndLen[1]
                            ruleType = clssAndLen[2]
                            afterBracket = clssAndLen[3]

                            if lenClassSpec > 2:
                                for i, clsSp in enumerate(classSpecification):
                                    if clsSp == '**' or clsSp == '*':
                                        continue
                                    if app.isInPackageStructure(clsSp):
                                        ret.append(ruleType[i] + clsSp + ' ' + afterBracket + ' ## is app specific rule ' + app.getName())

                                    ret.append(ruleType[i] + clsSp + ' ' + afterBracket)
                                continue

                            elif lenClassSpec == 2:
                                extendingClass = classSpecification[0]
                                classBeingExtended = classSpecification[1]
                                if app.isInPackageStructure(extendingClass)\
                                        or app.isInPackageStructure(classBeingExtended):
                                    rule = rule + ' ## is app specific rule ' + app.getName()
                                    #continue

                            elif lenClassSpec == 1:
                                classLocationReference = classSpecification[0]
                                if (len(classLocationReference.split('.')) == 1
                                    and classLocationReference.split('.')[0] == '**') \
                                        or (len(classLocationReference.split('.')) == 2
                                            and classLocationReference.split('.')[1] == '**'):
                                    continue
                                if app.isInPackageStructure(classLocationReference):
                                    rule = rule + ' ## is app specific rule ' + app.getName()
                                    #continue
                            else:
                                continue

                            ret.append(rule)
            return ret
        except UnicodeDecodeError:
            print('*************************  unicode decode error: no se puede leer las reglas\n\n' + path + '\n\n')

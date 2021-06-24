import re


def isolate_class_specifications(rule):
    ret = []

    class_specification_rules = ['keep', 'keepclassmembers', 'keepclasseswithmembers', 'keepnames',
                                 'keepclassmembernames', 'keepclasseswithmembernames', 'dontwarn', 'dontnote']
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
        classLocationReference = rule.split(' {', 1)[0].rsplit(' ', 1)

        if len(classLocationReference) < 2:
            return []
        classLocationReference = classLocationReference[1]

        ret.append(classLocationReference)

    annotations = re.findall('@(.*?) ', rule)
    if annotations:
        for ann in annotations:
            ret.append(ann)

    return ret


class ProGuard:
    """
    Clase que modela un archivo proguard.
    """

    def __init__(self, path, app):
        self.name = path.split('/')[-1]
        self.path = path
        self.defaultFile = (self.name == 'proguard-rules.pro')
        self.rules = Rules(self.findFileRules(path, app))

    def getRules(self):
        return self.rules.rules

    # funcion find Rules
    #
    # recive: path de la aplicacion y objeto aplicacion
    #
    # retorna: reglas de ofuscacion
    def findFileRules(self, path: str, app):

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

                            classSpecification = isolate_class_specifications(rule)
                            lenClassSpec = len(classSpecification)

                            if lenClassSpec == 2:
                                extendingClass = classSpecification[0]
                                classBeingExtended = classSpecification[1]
                                if app.isInPackageStructure(extendingClass)\
                                        or app.isInPackageStructure(classBeingExtended):
                                    rule = rule + '## is app specific rule ' + app.getName()

                            elif lenClassSpec == 1:
                                classLocationReference = classSpecification[0]
                                if (len(classLocationReference.split('.')) == 1
                                    and classLocationReference.split('.')[0] == '**') \
                                        or (len(classLocationReference.split('.')) == 2
                                            and classLocationReference.split('.')[1] == '**'):
                                    continue
                                if app.isInPackageStructure(classLocationReference):
                                    rule = rule + '## is app specific rule ' + app.getName()
                            else:
                                continue

                            ret.append(rule)
            return ret
        except UnicodeDecodeError:
            print('*************************  unicode decode error: no se puede leer las reglas\n\n' + path + '\n\n')


class Rules:

    def __init__(self, rules):
        self.rules = rules

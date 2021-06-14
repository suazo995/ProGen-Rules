import javalang


class AppClassAnalyser:

    def __init__(self, clss):
        self.clss = clss

    def detectDataClass(self, prnt=False):
        cls = self.clss

        fieldDecalrations = 0
        constructorDecarations = 0
        methodThatReturnsDeclarations = 0

        classCode = cls.getCode()
        tokens = javalang.tokenizer.tokenize(classCode)
        parser = javalang.parser.Parser(tokens)

        tree = parser.parse()

        for elm in tree.types[0].body:
            if isinstance(elm, javalang.tree.FieldDeclaration):
                if 'final' not in elm.modifiers:
                    fieldDecalrations += 1

                if prnt: print('Modifiers:', elm.modifiers, ', Type:', elm.type.name)
                for dec in elm.declarators:
                    if prnt: print(dec.name)

            if isinstance(elm, javalang.tree.ConstructorDeclaration):

                constructorDecarations += 1

                if prnt: print(elm.name)
                for param in elm.parameters:
                    if prnt: print('\t', param.name, param.type.name)

            if isinstance(elm, javalang.tree.MethodDeclaration):

                has_returns = False
                null = False
                override = False

                if prnt: print(elm.name)
                for path, node in elm.filter(javalang.tree.ReturnStatement):
                    has_returns = True
                    if isinstance(node.expression, javalang.tree.Literal) and node.expression.value == "null":
                        null = True

                for ann in elm.annotations:
                    if ann.name == "Override":
                        override = True

                if has_returns and not null and not override:
                    methodThatReturnsDeclarations += 1

            if prnt: print('--')
        extends = isinstance(tree.types[0], javalang.tree.ClassDeclaration) and isinstance(tree.types[0].extends,
                                                                                           javalang.tree.ReferenceType)
        return (fieldDecalrations * 2 >= methodThatReturnsDeclarations or extends) \
            and methodThatReturnsDeclarations >= fieldDecalrations * 0.75\
            and (fieldDecalrations > 0 or extends)\
            and methodThatReturnsDeclarations > 0 \
            and constructorDecarations > 0

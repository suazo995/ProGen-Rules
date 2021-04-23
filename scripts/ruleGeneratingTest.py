if __name__ == '__main__':
    from classes.Tester import Tester

    pathsForComparison = Tester.ruleGeneratingTestObject()
    Tester.ruleGeneratingTestDB(pathsForComparison)

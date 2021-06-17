from classes.DBConnect import DBConnect
if __name__ == '__main__':
    from classes.Tester import Tester

    # Tester.ruleGeneratingTestObject(percentage=10, pathToRepo='/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps', timesToAverage=50)
    Tester.ruleGeneratingTestDB(percentage=20)
    # Tester.ruleGeneratingTestDB(DBConnect('root', 'Juan.suaz0'), timesToAverage=1, percentage=10, specificAppsToTest=['/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF'])

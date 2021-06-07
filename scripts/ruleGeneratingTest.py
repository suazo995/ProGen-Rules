from classes.DBConnect import DBConnect
if __name__ == '__main__':
    from classes.Tester import Tester

    Tester.ruleGeneratingTestDB(percentage=10)
    #Tester.ruleGeneratingTestDB(['/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/MyExpenses'],DBConnect('root', 'Juan.suaz0'), timesToAverage=1)

import mysql.connector
from getpass import getpass


class DBConnect:

    def __init__(self, user = None, pswd = None):
        if user is None:
            user = input("Enter database user: ")
        if pswd is None:
            pswd = getpass("Enter database password: ")
        self.db = mysql.connector.connect(
            host="localhost",
            user=user,
            password=pswd,
            database="ReglasProguard"
        )
        self.cursor = self.db.cursor()

        sql = '''SET GLOBAL group_concat_max_len = 1000000;'''
        self.cursor.execute(sql)  # ejecuto la consulta
        self.db.commit()  # modifico la base de datos

    def close(self):
        self.db.close()

    def saveApp(self, app):
        data = (app.getName(), app.getPath(), app.getDontObfuscateRule(),
                len(app.getRules()), len(app.rulesForDeps()))

        sql = '''
                INSERT INTO Aplicacion (nombre, path, dontObf, numero_reglas, numero_reglas_deps)
                VALUES (%s, %s, %s, %s, %s)
                '''
        self.cursor.execute(sql, data)  # ejecuto la consulta
        self.db.commit()  # modifico la base de datos

        return self.cursor.lastrowid

    def saveDeps(self, appId, deps):
        for dep in deps:
            data = (dep, appId)

            sql = '''
                    INSERT INTO Dependencia (dep, appId)
                    VALUES (%s, %s)
                    '''
            self.cursor.execute(sql, data)  # ejecuto la consulta
            self.db.commit()  # modifico la base de datos

    def saveRules(self, appId, rules):
        for rule in rules:
            data = (rule, appId)

            sql = '''
                    INSERT INTO Regla (rule, appId)
                    VALUES (%s, %s)
                    '''
            self.cursor.execute(sql, data)  # ejecuto la consulta
            self.db.commit()  # modifico la base de datos

    def saveImports(self, appId, imports):
        for imp in imports:
            data = (imp, appId)

            sql = '''
                    INSERT INTO Import (imp, appId)
                    VALUES (%s, %s)
                    '''
            self.cursor.execute(sql, data)  # ejecuto la consulta
            self.db.commit()  # modifico la base de datos

    def getAppsWithDeps(self, dependencies):

        sqlAuxDeps = "("
        sqlAuxImports = "("
        for indx, dep in enumerate(dependencies):
            sqlAuxDeps = sqlAuxDeps + "dependencia.dep=\"" + dep + "\""
            sqlAuxImports = sqlAuxImports + "import.imp LIKE \"%" + dep + "%\""
            if indx<len(dependencies)-1:
                sqlAuxDeps = sqlAuxDeps + " OR "
                sqlAuxImports = sqlAuxImports  + " OR "
            else:
                sqlAuxDeps = sqlAuxDeps + ")"
                sqlAuxImports = sqlAuxImports + ")"

        sql ='''SELECT A.nombre, A.dependencias, A.reglas, GROUP_CONCAT(import.imp SEPARATOR '%')
                FROM
                (SELECT app.nombre, app.id, app.dependencias, GROUP_CONCAT(regla.rule SEPARATOR '%') as reglas
                FROM 
                (SELECT aplicacion.nombre as nombre, aplicacion.id as id, 
                GROUP_CONCAT(dependencia.dep SEPARATOR '%') as dependencias
                FROM 
                aplicacion JOIN dependencia
                WHERE dependencia.appId=aplicacion.id AND ''' + sqlAuxDeps + ''' GROUP BY aplicacion.id) as app 
                JOIN regla 
                WHERE app.id=regla.appId GROUP BY app.id) as A JOIN import
                WHERE A.id=import.appId AND ''' + sqlAuxImports + ''' GROUP BY A.id'''

        try:
            resultado = self.cursor.execute(sql)
            messages = self.cursor.fetchall()

            return messages
        except mysql.connector.Error as e:
            print('ERROR CONEXION AL LEER', e)

    def getAppsToTest(self, timesToAverage=50):
        sql = ''' 
                SELECT ReglasProguard.Aplicacion.nombre, ReglasProguard.Aplicacion.path 
                FROM ReglasProguard.Aplicacion JOIN ReglasProguard.Dependencia
                WHERE 
                ReglasProguard.Aplicacion.id = ReglasProguard.Dependencia.appId
                AND ReglasProguard.Aplicacion.numero_reglas_deps>1
                GROUP BY ReglasProguard.Aplicacion.id
                HAVING COUNT(ReglasProguard.Dependencia.id)>1
                ORDER BY RAND()
                LIMIT ''' + str(timesToAverage)

        pathsReturn = []

        try:
            resultado = self.cursor.execute(sql)
            messages = self.cursor.fetchall()

            for msg in messages:
                pathsReturn.append(msg[1])
            return pathsReturn
        except mysql.connector.Error as e:
            print('ERROR CONEXION AL LEER', e)
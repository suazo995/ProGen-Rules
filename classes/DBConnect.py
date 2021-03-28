import mysql.connector

class DBConnect:

    def __init__(self, user, password):
        self.db = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database="ReglasProguard"
        )
        self.cursor = self.db.cursor()

    def saveApp(self, app):
        data = (app.getName(), app.getPath(), app.getDontObfuscateRule())

        sql = '''
                INSERT INTO Aplicacion (nombre, path, dontObf)
                VALUES (%s, %s, %s)
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

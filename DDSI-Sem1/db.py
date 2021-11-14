import pyodbc
import json

# Driver MySql Server
CONNECTION_STRING = "DRIVER=ODBC Driver MySQL;server={0};uid={1};pwd={2};database={3}"

print(pyodbc.drivers())


class MySQLDB:

    def __init__(self):
        self.connection = None

    def connect(self, url='localhost', user='admin', passwd='admin', db='database', file=None):
        if file:
            with open(file, 'r+') as f:
                data = json.load(f)

                url = data['url']
                user = data['user']
                passwd = data['passwd']
                db = data['database']

        credentials = CONNECTION_STRING.format(url, user, passwd, db)
        self.connection = pyodbc.connect(credentials, autocommit=True)
        self.connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        self.connection.setencoding(encoding='utf-8')

    def get_cursor(self):
        return self.connection.cursor()

    def selectAll(self, table):
        cursor = self.connection.cursor()
        cursor.execute('select * from ' + table)
        return cursor

    def insert(self, table, values):
        INSERT_SENTENCE = "insert into {0} values ( {1} );"
        str_vals = "?, " * (len(values) - 1) + "?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(INSERT_SENTENCE.format(table, str_vals), tuple(values))
            cursor.close()
            return True
        except Exception as e:
            print('Error: ', e)
            return False

    def close(self):
        self.connection.close()

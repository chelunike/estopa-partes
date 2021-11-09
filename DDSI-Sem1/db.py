
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
        self.connection = pyodbc.connect(credentials)
        self.connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        self.connection.setencoding(encoding='utf-8')

        print(self.connection)

    def execute(self, sql, *args, **kwargs):
        cursor = self.connection.cursor()
        cursor.execute(sql, *args, **kwargs)
        return cursor

    def insert(self, table, values):
        INSERT_SENTENCE = "insert into {table} values ({values})"
        str_vals = ''
        for v in values:
            str_vals += '?,'
        cursor = self.execute(INSERT_SENTENCE.format(table=table, values=values), *values)
        if cursor.rowcount != len(values):
            print('ERROR')
        return cursor


    def close(self):
        self.connection.close();

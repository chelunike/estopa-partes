
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

    def close(self):
        self.connection.close();

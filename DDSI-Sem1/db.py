import pyodbc
import json

# Driver MySql Server
CONNECTION_STRING = "DRIVER=ODBC Driver MySQL;server={0};uid={1};pwd={2};database={3}"
#CONNECTION_STRING = "DRIVER=MySQL ODBC 8.0 ANSI Driver;server={0};uid={1};pwd={2};database={3}"

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

    def select(self, table, id, id_name='id'):
        try:
            data={}
            cursor = self.connection.cursor()
            cursor.execute(f'select * from {table} where {id_name}=?', (id))

            row = cursor.fetchone()
            for i in range(len(cursor.description)):
                data[cursor.description[i][0]] = row[i]
            cursor.close()
            return data
        except Exception as e:
            print('Error: ', e)
            return None

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

    def update(self, table,id, data, id_name='id'):
        UPDATE_SENTENCE = 'UPDATE {0} SET {1} WHERE {2}=?'
        str_vals = ''
        values = []
        for name, value in data.items():
            str_vals += f'{name}=?,'
            values.append(value)
        values.append(id)
        str_vals = str_vals[:len(str_vals)-1] # Eliminar la coma final
        try:
            cursor = self.connection.cursor()
            cursor.execute(UPDATE_SENTENCE.format(table, str_vals, id_name), values)
            cursor.close()
            return True
        except Exception as e:
            print('Error: ', e)
            return False

    def delete(self, table, id, id_name='id'):
        DELETE_SENTENCE = 'DELETE FROM {0} WHERE {1}=?'
        try:
            cursor = self.connection.cursor()
            cursor.execute(DELETE_SENTENCE.format(table, id_name), (id))
            cursor.close()
            return True
        except Exception as e:
            print('Error: ', e)
            return False

    def set_autocommit(self, auto):
        self.connection.autocommit = auto

    def close(self):
        self.connection.close()

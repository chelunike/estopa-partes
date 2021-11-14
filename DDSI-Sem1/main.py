#!/usr/bin/python3

from flask import Flask, request, render_template, redirect, session
import json
import os

import db

# -- Config Values --
CREDENTIALS_FILE = 'credentials.json'
DATA_FILE = 'sampleData.json'
RESET_SQL_FILE = 'mysql.sql'

# Conectamos con la base de datos
database = db.MySQLDB()
database.connect(file=CREDENTIALS_FILE)

# Iniciamos el servidor web
app = Flask('EstoParts', static_url_path='/assets', static_folder='templates/assets/')
app.secret_key = os.urandom(12).hex()


@app.route('/')
def index():
    data = {
        'title': 'Tabla de stock',
        'table': database.selectAll('stock')
    }
    if 'noty' in session.keys():
        data['noty'] = session['noty']

    return render_template('index.html', **data)


@app.route('/pedido')
def pedido():
    data = {
        'title': 'Tabla de pedidos',
        'table': database.selectAll('pedido'),
        'table_detalle':database.selectAll('detalle_pedido').fetchall()
    }
    if 'noty' in session.keys():
        data['noty'] = session['noty']

    return render_template('index.html', **data)


@app.route('/insert/stock', methods=['GET', 'POST'])
def insert_stock():
    data = {
        'title': 'Insertar stock'
    }

    if request.method == 'POST' and 'Cproducto' in request.form.keys() and 'Cantidad' in request.form.keys():
        type, msg = ('error',  'Error al insertar datos.')
        if database.insert('stock', [request.form['Cproducto'], request.form['Cantidad']]):
            type, msg = ('success', "Datos insertados correctamente :)")
        data['noty'] = [{
            'type': type,
            'msg': msg
        }]
    return render_template('insert-stock.html', **data)


@app.route('/edit/stock/<int:id>', methods=['GET', 'POST'])
def update_stock(id):
    data = {
        'title': f'Editar stock {id}'
    }
    if request.method == 'POST' and 'Cproducto' in request.form.keys() and 'Cantidad' in request.form.keys():
        type, msg = ('error', f'Error al editar datos del stock {id}.')
        changes = {
            'Cproducto': request.form['Cproducto'],
            'Cantidad': request.form['Cantidad']
        }
        if database.update('stock', id, changes, id_name='Cproducto'):
            type, msg = ('success', "Datos actualizados correctamente :)")
        data['noty'] = [{
            'type': type,
            'msg': msg
        }]
    row = database.select('stock', id, id_name='Cproducto')
    data.update(row)
    return render_template('insert-stock.html', **data)


@app.route('/delete/stock/<int:id>')
def delete_stock(id):
    type, msg = ('error', f'Error al borrar el stock {id}.')
    if database.delete('stock', id, id_name='Cproducto'):
        type, msg = ('success', "Datos insertados correctamente :)")
    session['noty'] = [{
        'type': type,
        'msg': msg
    }]
    return redirect('/')


@app.route('/delete/all', methods=['GET', 'POST'])
def delete_all():
    sql = ''
    with open(RESET_SQL_FILE, 'r+') as file:
        sql_lines = file.readlines()
        for line in sql_lines:
            if not line.startswith('--'):
                sql += line + '\n'
    cursor = database.get_cursor()
    sql = sql.replace("\n", "")
    sql = sql.replace("\t", "")
    for clause in sql.split(';'):
        if clause.strip() != '':
            print('CLAUSULA: ', clause.strip())
            cursor.execute(clause.strip())
    insert_sample_data()

    session['noty'] = [{
        'type': 'success',
        'msg': 'Tablas eliminadas y creadas correctamente'
    }]
    return redirect('/')


def insert_sample_data():
    with open(DATA_FILE, 'r+') as file:
        data = json.load(file)
        for table, rows in data.items():
            tableData = database.selectAll(table).fetchall()
            if len(tableData) <= 0:
                print('Insertando datos de ejemplo en: ', table)
                for row in rows:
                    database.insert(table, row)


if __name__ == '__main__':
    insert_sample_data()

    app.run('0.0.0.0', 8000, debug=True)

    database.close()



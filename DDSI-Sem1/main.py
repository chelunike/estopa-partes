#!/usr/bin/python3

from flask import Flask, render_template
import db

# Conectamos con la base de datos
database = db.MySQLDB()
database.connect(file='credentials.json')

# Iniciamos el servidor web
app = Flask('EstoParts')

@app.route('/')
def index():
    data = {
        'title': 'Tabla de stock',
        'table': database.selectAll('stock')
    }

    return render_template('index.html', **data)

@app.route('/pedido')
def pedido():
    data = {
        'title': 'Tabla de pedidos',
        'table': database.selectAll('pedido')
    }

    return render_template('index.html', **data)

@app.route('/insert/stock')
def insert_stock():
    data = {
        'title': 'Insertar stock'
    }

    return render_template('edit.html', **data)


app.run('0.0.0.0', 8000)
database.close()

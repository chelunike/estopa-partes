#!/usr/bin/python3

from flask import Flask, render_template
import db

app = Flask('EstoParts')

@app.route('/')
def index(request):
    data = {
        'title': 'Titulo'
    }

    return render_template('index.html', data)


#app.run('0.0.0.0', 8000)

database = db.MySQLDB()
database.connect(file='credentials.json')



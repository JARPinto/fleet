import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect


app = Flask(__name__)
app.config['SECRET KEY'] = 'JARPinto_13/07/1994'

# This can go to other file
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    db = get_db_connection()
    users = db.execute('SELECT * FROM users').fetchall()
    db.close()
    return render_template('index.html', posts=posts)

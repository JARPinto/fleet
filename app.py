from crypt import methods
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.secret_key = 'cfe12ea8ea6274e9d0ec84af142c2f93d2eff31469567670'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/register', methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")
        pwd = request.form.get("password")
        pwd_confirm = request.form.get("confirmation")
        print(name)
        print(pwd)
        print(pwd_confirm)
        if not name:
            flash('Username is required!')
            print('Username is required!')
        elif not pwd:
            flash('Password is required!')
            print('Password is required!')
        elif not pwd_confirm:
            flash('Confirmation password is required!')
            print('Confirmation password is required!')
        else:
            db = get_db_connection()
            db.execute('INSERT INTO users (username, hash) VALUES (?, ?)',
                        (name, pwd))
            db.commit()
            db.close()
            return redirect(url_for('index'))

    return render_template("register.html")
        

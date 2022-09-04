from crypt import methods
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
app.secret_key = 'cfe12ea8ea6274e9d0ec84af142c2f93d2eff31469567670'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
        # Get variables
        name = request.form.get("username")
        pwd = request.form.get("password")
        pwd_confirm = request.form.get("confirmation")
        print(name)
        print(pwd)
        print(pwd_confirm)
        # Check variables
        if not name:
            flash('Username is required!')
        elif not pwd:
            flash('Password is required!')
        elif not pwd_confirm:
            flash('Confirmation password is required!')
        else:
            # Hash password and save to db.
            pwd_hash = generate_password_hash(pwd, method='pbkdf2:sha256', salt_length=8)

            try:
                db = get_db_connection()
                cursor = db.cursor()
                print("Successfully Connected to SQL")

                cursor.execute('INSERT INTO users (username, hash) VALUES (?, ?)',
                            (name, pwd_hash))
                
                db.commit()
                print("Record inserted successfully", cursor.rowcount)
                cursor.close()
                return redirect(url_for('index'))
            
            except sqlite3.Error as error:
                print("Failed to insert data", error)

            finally:
                if db:
                    db.close()
                    print("The db connection is closed")

    return render_template("register.html")
        
@app.route ("/login", methods=["POST", "GET"])
def login():
    """Log user in"""
    # Forget any username
    session.clear()

    # if form is submite
    if request.method == "POST":
        name = request.form.get("username")
        pwd = request.form.get("password")
        print("Login c/: " + name)
        print("Pass login: " + pwd)
        # Check variables
        if not name:
            flash('Username is required!')
        elif not pwd:
            flash('Password is required!')
        else:
            # Query database for username
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (name,))
            rows = cursor.fetchall()
            print("Database reading done")
            print(len(rows))

            # Ensures username and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], pwd):
                flash("Invalid username and/or password")

            else:
                # Remember username exists and password is correct
                session["username"] = rows[0]["username"]
                print("username and password correct")
                print(rows[0]["username"])
                
                # Redirect user to home page 
                return redirect("/")
    return render_template("login.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session["name"] = None
    #return redirect("/")
    return render_template("/logout.html")
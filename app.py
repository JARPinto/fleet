from __future__ import print_function
from crypt import methods
from functools import reduce
from pprint import pprint
import re
import sqlite3
from string import punctuation
from xml.sax.handler import feature_external_ges
from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)
app.secret_key = 'cfe12ea8ea6274e9d0ec84af142c2f93d2eff31469567670'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

RANKS = [
    "OF-9 Gen", "OF-8 TGen", "OF-7 MGen", "OF-6 BGen",
    "OF-5 Cor", "OF-4 TCor", "OF-3 Maj",
    "OF-2 Cap", "OF-1 Ten", "OF-1 Alf", "OF-D Asp",
    "OR-9 SMor", "OR-8 SCh", "OR-7 SAj", 
    "OR-6 1Sarg", "OR-5 2Sarg",
    "OR-5 Furr", "OR-5 2Furr",
    "OR-4 CSec", "OR-3 CAdj", "OR-2 1Cb", "OR-2 2Cb", "OR-1 Sold",
]

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
@login_required
def index():
    db = get_db_connection()
    transports = db.execute('SELECT * FROM transports').fetchall()
    db.close()
    return render_template('index.html', transports=transports)

@app.route('/register', methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Get variables
        bim = request.form.get("bim")
        pwd = request.form.get("password")
        pwd_confirm = request.form.get("confirmation")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        rank = request.form.get("rank")
        print(bim)
        print(pwd)
        print(pwd_confirm)
        # Check variables
        if not bim:
            flash('BIM is required!')
        elif not pwd:
            flash('Password is required!')
        elif not pwd_confirm:
            flash('Confirmation password is required!')
        elif not first_name:
            flash('First name is required!')
        elif not last_name:
            flash('Last name is required!')
        elif not rank:
            flash('Rank is required!')
        else:
            # Hash password and save to db.
            pwd_hash = generate_password_hash(pwd, method='pbkdf2:sha256', salt_length=8)

            db = get_db_connection()
            cursor = db.cursor()
            print("Successfully Connected to SQL")
            
            cursor.execute("SELECT * FROM soldiers WHERE bim = ?", (bim,))
            rows = cursor.fetchall()            
            
            if len(rows) == 0:
                try:
                    cursor.execute('INSERT INTO soldiers (bim, hash, first_name, last_name, rank) VALUES (?, ?, ?, ?, ?)',
                            (bim, pwd_hash, first_name, last_name, rank))
                    db.commit()
                    print("Record inserted successfully", cursor.rowcount)
                    cursor.close()
                    session["user_id"] = bim
                except sqlite3.Error as error:
                    print("Failed to insert data", error)
                finally:
                    if db:
                        db.close()
                        print("The db connection is closed")
                return redirect(url_for('index'))
            else:
                flash("BIM already exists")
                
    return render_template("register.html", ranks = RANKS)
        
@app.route ("/login", methods=["POST", "GET"])
def login():
    """Log user in"""
    # Forget any BIM
    session.clear()

    # if form is submite
    if request.method == "POST":
        bim = request.form.get("bim")
        pwd = request.form.get("password")
        print("Login c/: " + bim)
        print("Pass login: " + pwd)
        # Check variables
        if not bim:
            flash('BIM is required!')
        elif not pwd:
            flash('Password is required!')
        else:
            # Query database for BIM
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM soldiers WHERE bim = ?", (bim,))
            rows = cursor.fetchall()
            print("Database reading done")
            print(len(rows))
            cursor.close()
            if db:
                db.close()

            # Ensures BIM and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], pwd):
                flash("Invalid BIM and/or password")

            else:
                # Remember BIM exists and password is correct
                session["user_id"] = rows[0]["id"]
                print("BIM and password correct")
                print(rows[0]["id"])
                
                # Redirect user to home page 
                return redirect("/")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    #return redirect("/")
    print("Fez logout")
    # In the end -- render redirect('/')
    return render_template("/logout.html")

@app.route('/transports', methods=["POST", "GET"])
@login_required
def transports():
    ''' Transports log '''
    # Query database for fleet
    db = get_db_connection()
    cursor = db.cursor()
    plates = cursor.execute("SELECT * FROM fleet").fetchall()
    
    #for row in plates:
     #   print(row[0])
      #  print(row.keys())
       # print(row['km'])

    if request.method == "POST":
        user_id = session["user_id"]
        # Get template data
        plate = request.form.get("plate")
        km_init = request.form.get("km_init")
        km_final = request.form.get("km_final")
        gas = request.form.get("gas")
        
        # Query for fleet data
        fleet = cursor.execute("SELECT * FROM fleet WHERE plate = ?", (plate,)).fetchall()
        km_actual = fleet[0]["km"]
        
        if not plate:
            flash('Plate is required!')
        elif not km_init:
            flash('Km init is required!')
        elif not km_final:
            flash('Km final is required!')        
        elif not gas:
            flash('Gas is required! - If None insert 0')
        elif (int(km_init) - int(km_actual)) < 0:
            flash('Initial km not valid')
        elif (int(km_final) - int(km_init)) < 0:
            flash('Final km need to be higher than initial ones')
        else:
            km_tot = int(km_final) - int(km_init)
            
            user = cursor.execute("SELECT * FROM soldiers WHERE id = ?", (user_id,)).fetchall()
            first_name = user[0]['first_name']
            last_name = user[0]['last_name']
            name = first_name + " " + last_name
            #user[0]['first_name']
            #print(user[user_id])
            # FDXXXX

            try:
                cursor.execute('INSERT INTO transports (user_id, plate, kms, gas, name, bim, rank) VALUES (?, ?, ?, ?, ?, ?, ?)',
                                (user_id, plate, km_tot, gas, name, user[0]["bim"], user[0]["rank"], ))
                # Update SQL tables
                cursor.execute("UPDATE fleet SET km = ? WHERE plate = ?", (km_final, plate,))           
                db.commit()
                print("Record inserted successfully", cursor.rowcount) # Isto nem faz sentido pois só insiro uma entrada
                cursor.close()
            except sqlite3.Error as error:
                print("Failed to insert data", error)
            finally:
                if db:
                    db.close()
                    print("The db connection is closed")
                    return redirect(url_for('index'))
                else:
                    redirect('/')
                    
        return redirect('/')

    return render_template("transports.html", plates = plates)

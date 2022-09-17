from __future__ import print_function
from cgi import test
from crypt import methods
from functools import reduce
from operator import le
from pprint import pprint
import re
import sqlite3
from string import punctuation
from turtle import distance
from xml.sax.handler import feature_external_ges
from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import calendar
import numpy

from helpers import login_required, str_to_month

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


@app.route ("/login", methods=["POST", "GET"])
def login():
    """Log user in"""
    # Forget any session
    session.clear()

    # Form submited
    if request.method == "POST":
        bim = request.form.get("bim")
        pwd = request.form.get("password")
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
            cursor.close()
            if db:
                db.close()

            # Ensures BIM and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], pwd):
                flash("Invalid BIM and/or password")

            else:
                # Remember session with user_od
                session["user_id"] = rows[0]["id"]
                return redirect("/")
    # GET
    return render_template("login.html")



@app.route('/', methods=["POST", "GET"])
@login_required
def index():

    ''' Transports log '''
    # Query database for fleet
    db = get_db_connection()
    cursor = db.cursor()
    plates = cursor.execute("SELECT * FROM fleet").fetchall()
    
    if request.method == "POST":
        user_id = session["user_id"]
        print(user_id)
        # Get template data
        plate = request.form.get("plate")
        datestring = request.form.get("date")
        km_init = request.form.get("km_init")
        km_final = request.form.get("km_final")
        gas = request.form.get("gas")
     
        # Query for new transport input
        fleet = cursor.execute("SELECT * FROM fleet WHERE plate = ?", (plate,)).fetchall()
        
        if plate:
            km_actual = fleet[0]["km"]
        
        if not plate:
            flash('Plate is required!')
        elif not datestring:
            flash('Date is required!')
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
            # month = calendar.month_name[datetime.strptime(datestring, '%Y-%m-%d').month]
            month = datetime.strptime(datestring, '%Y-%m-%d').month
            month = '%02d' % month
            print(month)
            print(type(month))
            
            try:
                user = cursor.execute("SELECT * FROM soldiers WHERE id = ?", (user_id,)).fetchall()            
                first_name = user[0]["first_name"]
                last_name = user[0]['last_name']
                name = first_name + " " + last_name
            except sqlite3.Error as error:
                print("Failed to insert data", error)

            try:
                cursor.execute('INSERT INTO transports (user_id, date, month, plate, kms, gas, name, bim, rank) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                (user_id, datestring, month, plate, km_tot, gas, name, user[0]["bim"], user[0]["rank"], ))
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
        # End of new transport input

    ##################################
    # Open DB and vars
    db = get_db_connection()
    cursor = db.cursor()
    user_id = session["user_id"]

    
    ##################################
    # Table definition
    transports = db.execute('SELECT * FROM transports WHERE user_id = ? ORDER BY date DESC', (user_id, )).fetchmany(size=7)

    ##################################
    # Graph definition
    # Monthly data by user
    graph_data = cursor.execute('SELECT month, SUM(month), SUM(kms) FROM transports WHERE user_id = ? GROUP BY month', (user_id, )).fetchall()
    datas = [row[0] for row in graph_data]
    months = [str_to_month(data) for data in datas]
    totals_id = [row[1] for row in graph_data]
    # Still need to use this
    kms_id = [row[2] for row in graph_data]

    # 5 Most user vehicles
    # Need to make a circular graph now
    graph_data_vehicles = cursor.execute('SELECT plate, SUM(kms) FROM transports WHERE user_id = ? GROUP BY plate', (user_id, )).fetchmany(5)
    plates_name = [row[0] for row in graph_data_vehicles]
    plates_kms = [row[1] for row in graph_data_vehicles]
    
    db.close()

    return render_template('index.html', plates = plates, transports=transports, months=months, totals_id=totals_id,
                    kms_id=kms_id, plates_name=plates_name, plates_kms=plates_kms)
                    # kms_id=kms_id, count_id=count_id, tot_kms=tot_kms)

@app.route('/history')
@login_required
def history():
    db = get_db_connection()
    transports = db.execute('SELECT * FROM transports').fetchall()
    db.close()
    return render_template('history.html', transports=transports)

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db_connection()
    cursor = db.cursor()

    # Totals data
    transports = db.execute('SELECT MAX(id) as id , SUM(kms) as kms , SUM(gas) as gas FROM transports').fetchall()
    numb_tp = transports[0]['id']
    numb_kms = transports[0]['kms']
    numb_gas = transports[0]['gas']

    # Monthly data
    graph_data = cursor.execute("SELECT month, SUM(kms), SUM(gas), SUM(month) FROM transports GROUP BY month").fetchall()

    datas = [row[0] for row in graph_data]
    distances = [row[1] for row in graph_data]
    gas = [row[2] for row in graph_data]
    totals = [row[3] for row in graph_data]
    
    months = [str_to_month(data) for data in datas]
    db.close()

    return render_template('dashboard.html', distances=distances, months=months, fuel=gas, totals=totals,
                    numb_tp=numb_tp, numb_kms=numb_kms, numb_gas=numb_gas)

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
                    cursor.execute("SELECT * FROM soldiers WHERE bim = ?", (bim,))
                    rows = cursor.execute("SELECT * FROM soldiers WHERE bim = ?", (bim,)).fetchall()
                    cursor.close()
                    session["user_id"] = rows[0]["id"]
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
        
@app.route('/logout')
def logout():
    session.clear()
    #return redirect("/")
    print("Fez logout")
    # In the end -- render redirect('/')
    return render_template("/logout.html")

@app.route('/consumption', methods=["POST", "GET"])
@login_required
def consumption():
    db = get_db_connection()
    cursor = db.cursor()
    
    months = cursor.execute("SELECT month FROM transports GROUP BY month").fetchall()
    months_dt = [data[0] for data in months]
    months = [str_to_month(data) for data in months_dt]

    table_data = cursor.execute('SELECT plate, SUM(kms) as kms, SUM(gas) as gas FROM transports GROUP BY plate').fetchall()
    plates_name = [row[0] for row in table_data]
    plates_kms = [int(row[1]) for row in table_data]
    plates_gas = [int(row[2]) for row in table_data]
    
    # Populates vehicles consumption
    plates_consumption = []
    for i in range(len(plates_name)):
        result =  "{:.1f}".format(int(plates_gas[i]) * 100 / int(plates_kms[i]))
        plates_consumption.append(float(result))

    print(plates_name)
    print(plates_consumption)
        
    if request.method == 'POST':
        # Get month name and convert to str with 2digit
        month_name = request.form.get("month")
        month_number = datetime.strptime(month_name, '%B').month
        month_tdig = '{:02d}'.format(month_number)
        
        # Same table with filter option
        table_data = cursor.execute('SELECT plate, SUM(kms) as kms, SUM(gas) as gas FROM transports WHERE month=? GROUP BY plate', (month_tdig,)).fetchall()
        plates_name = [row[0] for row in table_data]
        plates_kms = [int(row[1]) for row in table_data]
        plates_gas = [int(row[2]) for row in table_data]
        
        # Populates vehicles consumption
        plates_consumption = []
        for i in range(len(plates_name)):
            result =  "{:.1f}".format(int(plates_gas[i]) * 100 / int(plates_kms[i]))
            plates_consumption.append(float(result))

        print(plates_name)
        print(plates_consumption)

        return render_template('consumption.html', month_name=month_name, months=months, table_data=table_data, consumption=plates_consumption, plates=plates_name)

    return render_template('consumption.html', month_name="All YEAR", months=months, table_data=table_data, consumption=plates_consumption, plates=plates_name)

@app.route('/fleet', methods=["POST", "GET"])
@login_required
def fleet():
    db = get_db_connection()
    cursor = db.cursor()
    fleets = cursor.execute('SELECT * FROM fleet').fetchall()

    types = cursor.execute('SELECT type, COUNT(type), SUM(km) FROM fleet GROUP by type').fetchall()
    type_name = [row[0] for row in types]
    type_count = [row[1] for row in types]

    brands = cursor.execute('SELECT brand, COUNT(brand), SUM(km) FROM fleet GROUP by brand').fetchall()
    brand_name = [row[0] for row in brands]
    brand_count = [row[1] for row in brands]

    return render_template('fleet.html', fleets=fleets, type_name=type_name, type_count=type_count, brand_name=brand_name, brand_count=brand_count)
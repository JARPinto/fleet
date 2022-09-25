# FleetManagment
#### Video Demo: https://youtu.be/R4D7uWOMHNU
#### Description:
This project intends to solve a fleet management problem, taking a hypothetical case of an Armed Force vehicle fleet. I took this project because it solves some daily life problems I face every day, being a fleet manager myself.
The purpose for this project is for both the driver and the fleet manager to access the statistics of the different trips. The driver can register a trip, access his last trips and charts with summary of his activity. The fleet manager can see the Dashboard and the state of all vehicles within the different logs.


## Table of Contents
* [Project Summary](#your-project-title)
* [Technologies Used](#technologies-used)
* [Documentation](#documentation)
* [Setup](#setup)
* [Database](#database)
* [Features](#features)
* [Screenshots](#screenshots)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)

  
## Technologies Used
- Python v3.10.4
- Flask 2.2.2
- Werkzeug 2.2.2
- Bootstrap  v5.2.0
- Chart.js v3.9.1
- chartjs-plugin-datalabels v2.1.0

## Documentation
- Python: https://docs.python.org/3.10/#
- Flask: https://flask.palletsprojects.com/en/2.2.x/
- Werkzeug: https://werkzeug.palletsprojects.com/en/2.2.x/
- Bootstrap: https://getbootstrap.com/docs/5.2/getting-started/introduction/
- Chart.js: https://www.chartjs.org/docs/latest/
- chartjs-plugin-datalabels: https://master--chartjs-plugin-datalabels.netlify.app/
- sqlite3: https://www.sqlite.org/docs.html

## Setup
In requirements.txt: 
>python3; datetime; calendar; Flask; Flask-Session; requests; sqlite3; bootstrap; chartjs; chartjs-plugin-datalabels

## Database
- soldiers
  - id (autoincrement)
  - bim, number of identity
  - hash - saves the hashed password
  - first_name and last_name saves First and Last name
  - rank saves the user rank
- fleet
  - id (autoincrement)
  - plate, vehicle lisense plate
  - brand, vehicle brand
  - type, vehicle type
  - km, vehicle actual km
- transports
  - id (autoincrement)
  - user_id, unique value from session
  - plate, vehicle lisense plate
  - km, distance done in the trip
  - gas, fuel added after trip
  - name | bim | rank, user data
  - date, day of trip
  - month, takes de month from date with 02 digits
                      
  
## Features
- Log in
- Register
- New Transport Form
- Last transports information
- User tranports activity in graph
- Dashboard with monthly fleet activity
- Year totals for fleet activity
- Consumptions by vehicle (year and month values)
- Fleet vehicles actual km
- Fleet vehicles summary in graphs
- History of user inputs
- Logout


## Usage
* [Login](#login-page)
* [Register](#register-page)
* [Index](#index-page)
* [Dashboard](#dashboard-page)
* [Consumption](#consumption-page)  
* [Fleet](#fleet-page)  
* [History](#history-page)  

### Login page
Decorated is made for login
First it cleans the session
```python
@app.route ("/login", methods=["POST", "GET"])
def login():
    """Log user in"""
    # Forget any session
    session.clear()
``` 
Then if Form submited, it checks if all form was completed  
```python
    # Form submited
    if request.method == "POST":
        bim = request.form.get("bim")
        pwd = request.form.get("password")
        # Check variables
        if not bim:
            flash('BIM is required!')
        elif not pwd:
            flash('Password is required!')
```
If these conditions are checked, it gets all info from soldier tables, and ensures that BIM and password are correct. In positive case it remembers the session["user_id"] as the bim loggin and returns / (aka /index)
```python
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
                # Remember session with user_id
                session["user_id"] = rows[0]["id"]
                return redirect("/")      
``` 
If no Form will always return the login html
```python
  # GET
    return render_template("login.html")
```

### Register page
Decorated is made for register. If method by post it will save the variables with requests from the form and check is all form was completed
```python
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
```
In case the form is well submited it will:
  1. Hash the password
  ```python
          else:
            # Hash password and save to db.
            pwd_hash = generate_password_hash(pwd, method='pbkdf2:sha256', salt_length=8)
  ```
  2. Connect to db and try to insert into the soldiers table the new register. It will save session as bim. Note that not all code is displayed
  ```python
            cursor.execute("SELECT * FROM soldiers WHERE bim = ?", (bim,))
            rows = cursor.fetchall()            
            
            if len(rows) == 0:
                try:
                    cursor.execute('INSERT INTO soldiers (bim, hash, first_name, last_name, rank) VALUES (?, ?, ?, ?, ?)',
                            (bim, pwd_hash, first_name, last_name, rank))
                    db.commit()
                    rows = cursor.execute("SELECT * FROM soldiers WHERE bim = ?", (bim,)).fetchall()
                    session["user_id"] = rows[0]["id"]
  ```
  3. It will redirect to index if new user or flash message if BIM already exists
  ```python
                return redirect(url_for('index'))
            else:
                flash("BIM already exists")
  ``` 

### Index page
* [Form part](#form-part)
* [Tables and Graphs](#tables-and-graphs)

After login or register the user is redirected to index page, where it is possible to do:
- Submit a new movement
- See the user's last transports
- Read charts with monthly info
- Read chart with most used vehicles

#### Form part
The code for index function starts with the definition of plates - a variable taken in the html form to select one of the different plates available.
When the form is submitted, it saves and checks the variables. In the meantime it saves the actual km of the vehicle chosen before to ensure the km are the corrected.
```python
  @app.route('/', methods=["POST", "GET"])
@login_required
def index():
    ''' New transport FORM '''
    # Query database for fleet
    db = get_db_connection()
    cursor = db.cursor()
    plates = cursor.execute("SELECT * FROM fleet").fetchall()
    
    if request.method == "POST":
        user_id = session["user_id"]
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
            month = datetime.strptime(datestring, '%Y-%m-%d').month
            month = '%02d' % month
  ```
If everything is checked, the new movement will be inserted into the transports table and the actual km of the vehicles used will be updated to the final km. (Note: not all code displayed)
```python
                cursor.execute('INSERT INTO transports (user_id, date, month, plate, kms, gas, name, bim, rank) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                (user_id, datestring, month, plate, km_tot, gas, name, user[0]["bim"], user[0]["rank"], ))
                # Update SQL tables
                cursor.execute("UPDATE fleet SET km = ? WHERE plate = ?", (km_final, plate,))     
```
It returns always the index page again

#### Tables and graphs
In the index function is to defined the tables and grapsh that are shown after in the [screenshots part](#screenshots).
1. Table
```python
    # Table definition
    transports = db.execute('SELECT * FROM transports WHERE user_id = ? ORDER BY date DESC', (user_id, )).fetchmany(size=7)  
```
2. Monthly graphs
```python
    # Graph definition
    # Monthly data by user
    graph_data = cursor.execute('SELECT month, SUM(month), SUM(kms) FROM transports WHERE user_id = ? GROUP BY month', (user_id, )).fetchall()
    datas = [row[0] for row in graph_data]
    months = [str_to_month(data) for data in datas]
    totals_id = [row[1] for row in graph_data]  
```  
3. Most used vehicles graph
```python
    # 5 Most user vehicles
    graph_data_vehicles = cursor.execute('SELECT plate, SUM(kms) FROM transports WHERE user_id = ? GROUP BY plate', (user_id, )).fetchmany(5)
    plates_name = [row[0] for row in graph_data_vehicles]
    plates_kms = [row[1] for row in graph_data_vehicles]
``` 
4. Template
```python
    return render_template('index.html', plates = plates, transports=transports, months=months, totals_id=totals_id,
                    kms_id=kms_id, plates_name=plates_name, plates_kms=plates_kms)  
```
5. Example of the script for the graphs
```js
<script>
  var ctx_km = document.getElementById("linechart_tot_id").getContext("2d");
  var linechart = new Chart(ctx_km, {
      type: "line",
      // Data
      data: {
          labels: {{ months | safe }}, // Safe is for populate
          datasets: [{
              backgroundColor: 'rgba(55, 174, 148, 0.81)',
              borderColor: "rgba(55, 174, 148, 0.81)",
              data: {{ totals_id | safe }},
              datalabels: {
                  align: 'end',
                  anchor: 'end',
              }
```

  
### Dashboard page
Dashboard page gives the user a monthly summary of all fleet vehicles in terms of: number of transports, distance done and fuel input and it shows the yearly total for all those items.
1. Totals data
```python
    # Totals data
    transports = db.execute('SELECT MAX(id) as id , SUM(kms) as kms , SUM(gas) as gas FROM transports').fetchall()
    numb_tp = transports[0]['id']
    numb_kms = transports[0]['kms']
    numb_gas = transports[0]['gas']
```
2. Months data
```python
    # Monthly data
    graph_data = cursor.execute("SELECT month, SUM(kms), SUM(gas), SUM(month) FROM transports GROUP BY month").fetchall()

    datas = [row[0] for row in graph_data]
    distances = [row[1] for row in graph_data]
    gas = [row[2] for row in graph_data]
    totals = [row[3] for row in graph_data]
    
    months = [str_to_month(data) for data in datas]
```
3. Render template
```python
    return render_template('dashboard.html', distances=distances, months=months, fuel=gas, totals=totals,
                    numb_tp=numb_tp, numb_kms=numb_kms, numb_gas=numb_gas)
```

  
### Consumption page
Consumption page has two phases:
  1. First time clicking - shows year totals (code below will show year totals)
  2. After applying the filter it will show the values for the month chosen
- Filter option for months - first time going to the page it shows the years totals
  ```python
      # Entry values to the form
    months = cursor.execute("SELECT month FROM transports GROUP BY month").fetchall()
    months_dt = [data[0] for data in months]
    months = [str_to_month(data) for data in months_dt]
  ```
- Table with all vehicles used and total distance and total fuel for each one
  ```python
      # Table with full year stats
    table_data = cursor.execute('SELECT plate, SUM(kms) as kms, SUM(gas) as gas FROM transports GROUP BY plate').fetchall()
  ```
  Only difference after filter
  ```python
      if request.method == 'POST':
        # Get month name and convert to str with 2digit
        month_name = request.form.get("month")
        month_number = datetime.strptime(month_name, '%B').month
        month_tdig = '{:02d}'.format(month_number)
        
        # Same table with filter option
        table_data = cursor.execute('SELECT plate, SUM(kms) as kms, SUM(gas) as gas FROM transports WHERE month=? GROUP BY plate', (month_tdig,)).fetchall()
  ```
  Same variables
  ```python
    plates_name = [row[0] for row in table_data]
    plates_kms = [int(row[1]) for row in table_data]
    plates_gas = [int(row[2]) for row in table_data]
  ```
- Bar graph with consumption (Lt/100km) by vehicle where variables are defined
  ```python
    # Populates vehicles consumption
    plates_consumption = []
    for i in range(len(plates_name)):
        result =  "{:.1f}".format(int(plates_gas[i]) * 100 / int(plates_kms[i]))
        plates_consumption.append(float(result))
  ```
  
### Fleet page
Fleet function has three main parts:
  1. Fleet table
  ```python
      fleets = cursor.execute('SELECT * FROM fleet').fetchall()
  ``` 
  2. Variable definition to Type graph
  ```python
    types = cursor.execute('SELECT type, COUNT(type), SUM(km) FROM fleet GROUP by type').fetchall()
    type_name = [row[0] for row in types]
    type_count = [row[1] for row in types]
  ```
  3. Variable definition to Brand graph
  ```python
    brands = cursor.execute('SELECT brand, COUNT(brand), SUM(km) FROM fleet GROUP by brand').fetchall()
    brand_name = [row[0] for row in brands]
    brand_count = [row[1] for row in brands]
  ```
  
  
  
### History page
Simply shows all inputs
  ```python
      transports = db.execute('SELECT * FROM transports').fetchall()
  ```
  
  
### Logout page
Clears the session and renders the template
  ```python
  @app.route('/logout')
  def logout():
    session.clear()
    return render_template("/logout.html")
  ```
  
  
## Screenshots
  #### Login
  ![Login template](/readme_img/login.png)
  #### Register
  ![Register template](/readme_img/register.png)
  #### Index - New User
  ![Index new user template](/readme_img/indexone.png)
  #### Index - Form and table
  ![Index normal user template](/readme_img/indextwo.png)
  #### Index - Charts
  ![Index charts template](/readme_img/indexthree.png)
  #### Dashboard - First part
  ![Dashboard top template](/readme_img/dashboardone.png)
  #### Dashboard - Second part
  ![Dashboard bottom template](/readme_img/dashboardtwo.png)
  #### Consumption - First part
  ![Consumption top template](/readme_img/consumptionone.png)
  #### Consumption - Second part
  ![Consumption middle template](/readme_img/consumptiontwo.png)  
  #### Consumption - Third part
  ![Consumption bottom template](/readme_img/consumptionthree.png)
  #### Fleet - First part
  ![Fleet top template](/readme_img/fleetone.png)  
  #### Fleet - Second part
  ![Fleet bottom template](/readme_img/fleettwo.png)
  #### History
  ![History template](/readme_img/history.png)
  #### Logout
  ![Logout template](/readme_img/logout.png)

## Project Status
- _complete_ / for CS50 final projetct submission 🎆
- _in progress_ with the aim to achieve the same as excel on daily work 
  
## Room for Improvement
### Room for improvement:
- Create different sessions for driver and manager, with different accessibilities
- Give opportunity for users to change their preferences
- Possibility to input older trips (for now it needs to be continuous)
- Export data from history inputs
- Create automatic reports based on the dashboard and consumption
- Create mantainemence page to update vehicles operacional viability
- Create QRCodes to all vehicles to apply new trip
- Management side -> insert new vehicles and correct trips from users (without going to database directly)
- Mobile phone support (specially drivers)
- Etc...

### To do:
- [X] Enjoy the process 😁
- [ ] Submit CS50 final project (🙏 hope I can manage this with this WebApp 😰)
- [ ] Do all the improvements above 💪


## Acknowledgements
- This project was inspired by daily work, doing this in excel
- This project was based on CS50 Finance
- This README was based on https://github.com/iharsh234/WebApp
- Many thanks to [CS50](https://pll.harvard.edu/course/cs50-introduction-computer-science?delta=0) team
- Special thanks to my lovely girlfriend for all the support in the way ❤️


## Contact
Created by 🪖José Pinto, 
           @Lisbon, Portugal 🇵🇹
           andre_pinto_10@hotmail.com - feel free to contact me!


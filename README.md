# YOUR PROJECT TITLE
#### Video Demo:  <URL HERE>
#### Description:
This project intend to solve the problem of fleet management, taking a hipotetic case of an Armed Force vehicle fleet. I took this project because it solves some daily life problems I face all day, being a fleet manager myself.
The purpose for this project is for both driver and fleet manager acess the statics of the different trips.
The driver can register a trip, acess his last trips and charts with summary of his activity. The fleet manage can see the Dashboard and the state of all vehicles within the different logs.


## Table of Contents
* [Project Summary](#your-project-title)
* [Technologies Used](#technologies-used)
* [Documentation](#documentation)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->

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

## Features
- Log in
- Register
- New transport Form
- Last transports information
- User tranports activity in graph
- Dashboard with monthly fleet activity
- Year totals for fleet activity
- Consumptions by vehicle (year and month values)
- Fleet vehicles actual km
- Fleet vehicles summary in graphs
- History of user inputs
- Logout



This application is divided in 5 structural points:
Static Folder
Templates Folder
App.py
database.db 
Requirements.txt - needs no introduction, basically shows the requirements to run the application

Static Folder as 03 subfolders:
  - css: contains 02 css files
      - bootstrap.min.css (https://getbootstrap.com/docs/5.2/getting-started/download/)
      - style.cc (definition of body and navbar style)
  - fig: contains 03 figures to use on the web app
  - js: contains 03 js files
      - bootstrap.min.js (https://getbootstrap.com/docs/5.2/getting-started/download/)
      - chart.min.js (https://www.chartjs.org/docs/latest/getting-started/installation.html)
      - chartjs-plugin-datalabels.min.js (https://github.com/chartjs/chartjs-plugin-datalabels/releases/tag/v2.1.0)
      
Database explanation:
  - "soldiers", saves id (autoincrement),
                      bim - number of identity, 
                      hash - saves the hashed password, 
                      first_name and last_name saves First and Last name,
                      rank saves the user rank
 
  - "fleet", saves id (autoincrement),
                      plate - vehicle lisence plate, 
                      brand - vehicle brand, 
                      type - vehicle type, 
                      km - vehicle actual km

  - "transports", saves id (autoincrement),
                        plate - vehicle lisence plate, 
                        brand - vehicle brand, 
                        type - vehicle type, 
                        km - vehicle actual km
                      

Templates folder as 08 html file:
  - base.html (this html file will be extended in all the other html files)
  
      














## Screenshots
![Example screenshot](./img/screenshot.png)
<!-- If you have screenshots you'd like to share, include them here. -->


## Setup
In requirements.txt: 
>python3;
datetime;
calendar;
Flask;
Flask-Session;
requests;
sqlite3;
bootstrap;
chartjs;
chartjs-plugin-datalabels


## Usage
How does one go about using it?
Provide various use cases and code examples here.

`write-your-code-here`


## Project Status
Project is: _in progress_ / _complete_ / _no longer being worked on_. If you are no longer working on it, provide reasons why.


## Room for Improvement
Include areas you believe need improvement / could be improved. Also add TODOs for future development.

Room for improvement:
- Improvement to be done 1
- Improvement to be done 2

To do:
- Feature to be added 1
- Feature to be added 2


## Acknowledgements
Give credit here.
- This project was inspired by...
- This project was based on [this tutorial](https://www.example.com).
- Many thanks to...


## Contact
Created by [@flynerdpl](https://www.flynerd.pl/) - feel free to contact me!

https://github.com/iharsh234/WebApp --- i came to drink here
<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->

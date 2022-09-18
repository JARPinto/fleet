# YOUR PROJECT TITLE
#### Video Demo:  <URL HERE>
#### Description:
This project is a web app designed to help..

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
                      
CREATE TABLE "transports" (
	"id"	INTEGER,
	"user_id"	TEXT NOT NULL,
	"plate"	NUMERIC NOT NULL,
	"kms"	INTEGER NOT NULL,
	"gas"	NUMERIC NOT NULL,
	"name"	TEXT NOT NULL,
	"bim"	INTEGER NOT NULL,
	"rank"	TEXT NOT NULL,
	"date"	TEXT NOT NULL,
	"month"	TEXT NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "soldiers"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);


Templates folder as 08 html file:
  - base.html (this html file will be extended in all the other html files)
  
      


Documentation:
Insert here the links to
- bootstrap
- chartjs
- chartjsplugins
- sqlite3
- flask

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
  - plate, vehicle lisence plate
  - brand, vehicle brand
  - type, vehicle type
  - km, vehicle actual km
- transports
  - id (autoincrement)
  - user_id, unique value from session
  - plate, vehicle lisence plate
  - km, distance done in the trip
  - gas, fuel added after trip
  - name | bim | rank, user data
  - date, day of trip
  - month, takes de month from date with 02 digits
                      
  
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


      




## Usage
How does one go about using it?
Provide various use cases and code examples here.



## Screenshots
  #### Login
  ![Login template](/readme_img/login.png)
  #### Register
  ![Login template](/readme_img/register.png)
  #### Index - New User
  ![Login template](/readme_img/indexone.png)
  #### Index - Form and table
  ![Login template](/readme_img/indextwo.png)
  #### Index - Charts
  ![Login template](/readme_img/indexthree.png)
  #### Dashboard - First part
  ![Login template](/readme_img/dashboardone.png)
  #### Dashboard - Second part
  ![Login template](/readme_img/dashboardtwo.png)
  #### Consumption - First part
  ![Login template](/readme_img/consumptionone.png)
  #### Consumption - Second part
  ![Login template](/readme_img/consumptiontwo.png)  
  #### Consumption - Third part
  ![Login template](/readme_img/consumptionthree.png)
  #### Fleet - First part
  ![Login template](/readme_img/fleetone.png)  
  #### Fleet - Second part
  ![Login template](/readme_img/fleettwo.png)
  #### History
  ![Login template](/readme_img/history.png)
  #### Logout
  ![Login template](/readme_img/logout.png)

## Project Status
- _complete_ / for CS50 final projetct submission 🎆
- _in progress_ with the aim to achieve the same as excel on daily work 
  
## Room for Improvement
### Room for improvement:
- Create different sessions for driver and management , with different accessibilities
- Give oportunity to users to change their preferences
- Possibility to input older trips (for now needs to be continuous)
- Export data from history inputs
- Create automatic reports based on the dashboard and consumption
- Create mantainemence page to update vehicles operacional viability
- Create QRCodes to all vehicles to aply new trip
- Management side -> inser new vehicles and correct trips from users (without going to database directly)
- Mobile phone suport (drives specially)
- Etc...

### To do:
- [X] Enjoy the process 😁
- [ ] Submit CS50 final project (🙏 hope I can manage this with this WebApp 😰)
- [ ] Do all the improvements above 💪


## Acknowledgements
- This project was inspired by daily work, doing this in excel
- This project was based on CS50 Finance
- This README was base on https://github.com/iharsh234/WebApp
- Many thanks to [CS50](https://pll.harvard.edu/course/cs50-introduction-computer-science?delta=0) team
- Special thanks to my lovely girlfriend for all the support in the way ❤️


## Contact
Created by 🪖José Pinto, 
           @Lisbon, Portugal 🇵🇹
           andre_pinto_10@hotmail.com - feel free to contact me!


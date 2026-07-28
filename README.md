# Bus Crowd Predictor

A simple web app built for my first-year Computer Science project.
It helps students and teachers check how crowded their college bus is,
lets drivers see who is waiting at each stop, and lets the transport
department manage bus routes.

## Problem Statement

College buses (especially the hostel route buses) are sometimes very
full and sometimes almost empty, but there was no way to know in
advance. Also, drivers sometimes skip boarding points because they
don't know students are waiting there. This project tries to solve
both problems with a simple reporting system.

## Features

- Simple username-based login (student / teacher / transport)
- Students & teachers confirm which bus and boarding point they're using
- Dashboard shows current seat availability, boarding history, and a
  simple prediction (based on historical averages, using Pandas — no
  machine learning)
- Driver view (no login) shows how many students are waiting at each
  boarding point today
- Transport department can add new buses and see a live summary of
  every bus

## Tech Stack

- Python (Flask) - backend and routing
- MySQL - database
- Pandas - historical average calculation for prediction
- HTML, CSS, Bootstrap - frontend
- JavaScript - minor form interactivity

## Project Structure

```
bus-crowd-predictor/
├── app.py              -> Main Flask app (all routes)
├── config.py            -> MySQL connection settings
├── database.sql          -> Creates database, tables, and bus route data
├── requirements.txt       -> Python packages needed
├── static/
│   └── css/style.css      -> Page styling
└── templates/
    ├── index.html          -> Login page
    ├── submit.html          -> Confirm boarding page (student/teacher)
    ├── dashboard.html        -> Seat status, history, prediction
    ├── driver.html            -> Driver view (per-stop counts)
    └── admin.html              -> Transport department page
```

## How to Run

1. Install MySQL and create the database:
   ```
   mysql -u root -p < database.sql
   ```

2. Create a virtual environment and install packages:
   ```
   python -m venv venv
   venv\Scripts\activate      (Windows)
   pip install -r requirements.txt
   ```

3. Open `config.py` and set your MySQL password.

4. Run the app:
   ```
   python app.py
   ```

5. Open `http://127.0.0.1:5000/` in your browser.

## How the Prediction Works

For a selected bus, the app pulls every past day's boarding count from
MySQL into a Pandas DataFrame, groups it by date, and calculates the
**average number of students per day**. That average is shown as the
predicted crowd for the next trip. This is a simple statistical
estimate, not a machine learning model.

## Possible Improvements

- Add real boarding point names per route
- Add password-based login
- Show prediction charts (using Matplotlib)

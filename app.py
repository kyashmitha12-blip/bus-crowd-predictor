# app.py
# Main Flask application file for Bus Crowd Predictor.
# Handles login, boarding submission, dashboard, driver view, and admin (transport) page.

from flask import Flask, render_template, request, session, redirect
import mysql.connector
import pandas as pd
from datetime import date, datetime
from config import DB_CONFIG

app = Flask(__name__)
# Secret key is needed for Flask sessions to work securely
app.secret_key = 'buscrowd_secret_key'

# Fixed list of boarding points used for every route (kept simple for this project)
BOARDING_POINTS = ['Stop 1', 'Stop 2', 'Stop 3']


# Helper function: opens a new MySQL connection using our config
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ---------- LOGIN PAGE ----------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']   # student, teacher, or transport

        # Save username and role in the session so other pages know who's logged in
        session['username'] = username
        session['role'] = role

        # Transport staff go to the admin page, everyone else goes to submit
        if role == 'transport':
            return redirect('/admin')
        else:
            return redirect('/submit')

    return render_template('index.html')


# Simple logout: clears the session
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------- SUBMIT / BOARDING CONFIRMATION PAGE (student & teacher) ----------
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    # If nobody is logged in, send them back to login
    if 'username' not in session:
        return redirect('/')

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        bus_number = request.form['bus_number']
        boarding_point = request.form['boarding_point']
        username = session['username']

        # Save this boarding confirmation with today's date and current time
        cursor.execute(
            "INSERT INTO bus_boarding (username, bus_number, boarding_point, travel_date, travel_time) "
            "VALUES (%s, %s, %s, %s, %s)",
            (username, bus_number, boarding_point, date.today(), datetime.now().time())
        )
        conn.commit()

    # Get the list of all buses to show in the dropdown
    cursor.execute("SELECT bus_number, route_name FROM bus_capacity ORDER BY bus_number")
    buses = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'submit.html',
        buses=buses,
        boarding_points=BOARDING_POINTS,
        username=session['username']
    )


# ---------- DASHBOARD PAGE (student & teacher) ----------
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect('/')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all buses for the dropdown
    cursor.execute("SELECT bus_number, route_name FROM bus_capacity ORDER BY bus_number")
    buses = cursor.fetchall()

    selected_bus = request.args.get('bus_number')

    total_seats = None
    occupied_today = 0
    available_seats = None
    history = []
    prediction = None
    route_name = None

    if selected_bus:
        # Get total seats for this bus
        cursor.execute("SELECT total_seats, route_name FROM bus_capacity WHERE bus_number = %s", (selected_bus,))
        bus_info = cursor.fetchone()
        if bus_info:
            total_seats = bus_info['total_seats']
            route_name = bus_info['route_name']

        # Count how many students/teachers boarded this bus today
        cursor.execute(
            "SELECT COUNT(*) AS cnt FROM bus_boarding WHERE bus_number = %s AND travel_date = %s",
            (selected_bus, date.today())
        )
        occupied_today = cursor.fetchone()['cnt']

        if total_seats is not None:
            available_seats = total_seats - occupied_today

        # Get previous reports (boarding history) for this bus, most recent first
        cursor.execute(
            "SELECT username, boarding_point, travel_date, travel_time FROM bus_boarding "
            "WHERE bus_number = %s ORDER BY travel_date DESC, travel_time DESC LIMIT 20",
            (selected_bus,)
        )
        history = cursor.fetchall()

        # ---- PREDICTION using Pandas ----
        # Get the count of boardings per day for this bus, from all history
        cursor.execute(
            "SELECT travel_date, COUNT(*) AS daily_count FROM bus_boarding "
            "WHERE bus_number = %s GROUP BY travel_date",
            (selected_bus,)
        )
        daily_counts = cursor.fetchall()

        if daily_counts:
            # Put the results into a Pandas DataFrame
            df = pd.DataFrame(daily_counts)
            # Simple prediction: average number of students per day, historically
            prediction = round(df['daily_count'].mean())
        else:
            prediction = 0

    cursor.close()
    conn.close()

    return render_template(
        'dashboard.html',
        buses=buses,
        selected_bus=selected_bus,
        route_name=route_name,
        total_seats=total_seats,
        occupied_today=occupied_today,
        available_seats=available_seats,
        history=history,
        prediction=prediction
    )


# ---------- DRIVER VIEW (no login needed) ----------
@app.route('/driver', methods=['GET'])
def driver():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT bus_number, route_name FROM bus_capacity ORDER BY bus_number")
    buses = cursor.fetchall()

    selected_bus = request.args.get('bus_number')
    stop_counts = []
    route_name = None

    if selected_bus:
        cursor.execute("SELECT route_name FROM bus_capacity WHERE bus_number = %s", (selected_bus,))
        info = cursor.fetchone()
        if info:
            route_name = info['route_name']

        # Count students waiting at each boarding point, for today
        cursor.execute(
            "SELECT boarding_point, COUNT(*) AS cnt FROM bus_boarding "
            "WHERE bus_number = %s AND travel_date = %s GROUP BY boarding_point",
            (selected_bus, date.today())
        )
        stop_counts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'driver.html',
        buses=buses,
        selected_bus=selected_bus,
        route_name=route_name,
        stop_counts=stop_counts
    )


# ---------- ADMIN / TRANSPORT PAGE ----------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Only transport staff can access this page
    if session.get('role') != 'transport':
        return redirect('/')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Adding a new bus route
        bus_number = request.form['bus_number']
        route_name = request.form['route_name']
        total_seats = request.form['total_seats']

        cursor.execute(
            "INSERT INTO bus_capacity (bus_number, route_name, total_seats) VALUES (%s, %s, %s)",
            (bus_number, route_name, total_seats)
        )
        conn.commit()

    # Show every bus with today's occupied/available count
    cursor.execute("SELECT bus_number, route_name, total_seats FROM bus_capacity ORDER BY bus_number")
    all_buses = cursor.fetchall()

    bus_summary = []
    for bus in all_buses:
        cursor.execute(
            "SELECT COUNT(*) AS cnt FROM bus_boarding WHERE bus_number = %s AND travel_date = %s",
            (bus['bus_number'], date.today())
        )
        occupied = cursor.fetchone()['cnt']
        bus_summary.append({
            'bus_number': bus['bus_number'],
            'route_name': bus['route_name'],
            'total_seats': bus['total_seats'],
            'occupied': occupied,
            'available': bus['total_seats'] - occupied
        })

    cursor.close()
    conn.close()

    return render_template('admin.html', bus_summary=bus_summary, username=session.get('username'))


if __name__ == '__main__':
    app.run(debug=True)

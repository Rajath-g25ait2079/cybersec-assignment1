"""
SQL Injection Demo Web Application
===================================
** FOR EDUCATIONAL PURPOSES ONLY **
** IIT Jodhpur - Cyber Security Assignment **

This application is DELIBERATELY VULNERABLE to SQL injection attacks.
It is designed to demonstrate all 3 types of SQL injection:
  1. In-Band SQLi (Error-based & Union-based)
  2. Blind SQLi (Boolean-based & Time-based)
  3. Out-of-Band SQLi (Simulated DNS/HTTP exfiltration)

NEVER deploy this on a public server. Run only in a controlled lab environment.
"""

import sqlite3
import os
import time
import json
from flask import Flask, request, render_template, redirect, url_for, jsonify, session

app = Flask(__name__)
app.secret_key = "insecure-demo-key-do-not-use-in-production"

DB_PATH = os.path.join("/tmp", "university.db")

# ── Out-of-Band exfiltration log (simulates attacker's DNS/HTTP server) ──
OOB_LOG_PATH = os.path.join("/tmp", "oob_exfil_log.json")


def get_db():
    """Get a raw SQLite connection (no ORM - intentionally vulnerable)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable custom functions for demo
    conn.create_function("sleep", 1, lambda secs: time.sleep(secs))
    conn.create_function("exfiltrate", 1, log_oob_exfiltration)
    return conn


def log_oob_exfiltration(data):
    """Simulates out-of-band data exfiltration (logs to a file instead of DNS/HTTP)."""
    entry = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "exfiltrated_data": str(data)}
    logs = []
    if os.path.exists(OOB_LOG_PATH):
        with open(OOB_LOG_PATH, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    logs.append(entry)
    with open(OOB_LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)
    return data


def init_db():
    """Initialize the database with sample student data."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        DROP TABLE IF EXISTS students;
        DROP TABLE IF EXISTS grades;
        DROP TABLE IF EXISTS admin_users;
        DROP TABLE IF EXISTS secret_flags;

        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            roll_number TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            semester INTEGER,
            password TEXT NOT NULL
        );

        CREATE TABLE grades (
            id INTEGER PRIMARY KEY,
            roll_number TEXT NOT NULL,
            course TEXT NOT NULL,
            grade TEXT NOT NULL,
            semester INTEGER
        );

        CREATE TABLE admin_users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            secret_notes TEXT
        );

        CREATE TABLE secret_flags (
            id INTEGER PRIMARY KEY,
            flag_name TEXT NOT NULL,
            flag_value TEXT NOT NULL
        );

        -- Sample students
        INSERT INTO students VALUES (1, 'G25AIT2052', 'Khushi Bawistale', 'khushi@iitj.ac.in', 'AI & Data Science', 2, 'khushi123');
        INSERT INTO students VALUES (2, 'G25AIT2100', 'Shashank Jangid', 'shashank@iitj.ac.in', 'AI & Data Science', 2, 'shashank456');
        INSERT INTO students VALUES (3, 'G25AIT2079', 'Rajath S M', 'rajath@iitj.ac.in', 'AI & Data Science', 2, 'rajath789');
        INSERT INTO students VALUES (4, 'G25AIT2105', 'Siddhant Singh', 'siddhant@iitj.ac.in', 'AI & Data Science', 2, 'siddhant101');
        INSERT INTO students VALUES (5, 'G25AIT2029', 'Deepanshu Arora', 'deepanshu@iitj.ac.in', 'AI & Data Science', 2, 'deepanshu202');
        INSERT INTO students VALUES (6, 'G25AIT2111', 'Soumya A', 'soumya@iitj.ac.in', 'AI & Data Science', 2, 'soumya303');
        INSERT INTO students VALUES (7, 'G25AIT2121', 'Shah Tirth Rajeshkumar', 'tirth@iitj.ac.in', 'AI & Data Science', 2, 'tirth404');
        INSERT INTO students VALUES (8, 'B20CS1010', 'Amit Kumar', 'amit@iitj.ac.in', 'Computer Science', 6, 'amit@secure');
        INSERT INTO students VALUES (9, 'B20EE2020', 'Priya Sharma', 'priya@iitj.ac.in', 'Electrical Engineering', 6, 'priya@pass');
        INSERT INTO students VALUES (10, 'B20ME3030', 'Rahul Verma', 'rahul@iitj.ac.in', 'Mechanical Engineering', 6, 'rahul@1234');

        -- Sample grades
        INSERT INTO grades VALUES (1, 'G25AIT2079', 'Cyber Security', 'A', 2);
        INSERT INTO grades VALUES (2, 'G25AIT2079', 'Machine Learning', 'A+', 2);
        INSERT INTO grades VALUES (3, 'G25AIT2079', 'Data Structures', 'A', 2);
        INSERT INTO grades VALUES (4, 'G25AIT2052', 'Cyber Security', 'A+', 2);
        INSERT INTO grades VALUES (5, 'G25AIT2100', 'Cyber Security', 'A', 2);
        INSERT INTO grades VALUES (6, 'B20CS1010', 'Database Systems', 'B+', 6);

        -- Admin users (sensitive - should not be accessible)
        INSERT INTO admin_users VALUES (1, 'admin', 'SuperSecret@2026', 'superadmin', 'Master password for all systems: IITJAdmin#2026');
        INSERT INTO admin_users VALUES (2, 'dean_academics', 'Dean@cademics2026', 'dean', 'Grade change requests pending review');
        INSERT INTO admin_users VALUES (3, 'registrar', 'Registrar@IITJ', 'registrar', 'New admission data backup at /secure/backups');

        -- Secret flags (CTF-style for fun during demo)
        INSERT INTO secret_flags VALUES (1, 'FLAG_INBAND', 'IITJ{in_band_sqli_union_attack_success}');
        INSERT INTO secret_flags VALUES (2, 'FLAG_BLIND', 'IITJ{blind_sqli_boolean_time_based_win}');
        INSERT INTO secret_flags VALUES (3, 'FLAG_OOB', 'IITJ{out_of_band_exfiltration_complete}');
    """)

    conn.commit()
    conn.close()
    # Clear OOB log
    if os.path.exists(OOB_LOG_PATH):
        os.remove(OOB_LOG_PATH)
    print("[*] Database initialized with sample data.")


# ══════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════

@app.route("/")
def home():
    """IIT Jodhpur styled homepage."""
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    LOGIN PAGE - VULNERABLE TO IN-BAND SQL INJECTION
    The username and password are directly concatenated into the SQL query.
    """
    error = None
    debug_query = None
    result_data = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # !! DELIBERATELY VULNERABLE - Direct string concatenation !!
        query = f"SELECT * FROM students WHERE roll_number = '{username}' AND password = '{password}'"
        debug_query = query  # Show query for educational purposes

        conn = get_db()
        try:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            if rows:
                result_data = [dict(row) for row in rows]
                session["logged_in"] = True
                session["user"] = result_data[0]["name"]
                session["roll"] = result_data[0]["roll_number"]
                return render_template("dashboard.html", user=result_data[0], all_results=result_data, query=debug_query)
            else:
                error = "Invalid Roll Number or Password."
        except Exception as e:
            # !! DELIBERATELY EXPOSING ERROR MESSAGES (Error-based SQLi) !!
            error = f"Database Error: {str(e)}"
        finally:
            conn.close()

    return render_template("login.html", error=error, query=debug_query)


@app.route("/search", methods=["GET"])
def search_student():
    """
    STUDENT SEARCH - VULNERABLE TO BLIND SQL INJECTION
    This endpoint only returns "Found" or "Not Found" (no data leakage in response),
    making it a perfect target for Boolean-based and Time-based blind SQLi.
    """
    roll = request.args.get("roll", "")
    result = None
    debug_query = None
    response_time = None

    if roll:
        query = f"SELECT roll_number FROM students WHERE roll_number = '{roll}'"
        debug_query = query

        conn = get_db()
        start_time = time.time()
        try:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            elapsed = round(time.time() - start_time, 3)
            response_time = elapsed
            if rows:
                result = "Student Found"
            else:
                result = "Student Not Found"
        except Exception as e:
            elapsed = round(time.time() - start_time, 3)
            response_time = elapsed
            result = f"Error: {str(e)}"
        finally:
            conn.close()

    return render_template("search.html", roll=roll, result=result, query=debug_query, response_time=response_time)


@app.route("/profile")
def profile():
    """
    STUDENT PROFILE - VULNERABLE TO UNION-BASED SQL INJECTION
    Fetches student profile by ID parameter.
    """
    student_id = request.args.get("id", "")
    student = None
    debug_query = None
    error = None
    raw_results = None

    if student_id:
        query = f"SELECT id, roll_number, name, email, department, semester FROM students WHERE id = {student_id}"
        debug_query = query

        conn = get_db()
        try:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            raw_results = [list(row) for row in rows]
            if rows:
                student = dict(rows[0])
        except Exception as e:
            error = f"Database Error: {str(e)}"
        finally:
            conn.close()

    return render_template("profile.html", student=student, query=debug_query, error=error, raw_results=raw_results)


@app.route("/oob_demo", methods=["GET", "POST"])
def oob_demo():
    """
    OUT-OF-BAND SQLi DEMO
    Uses a custom SQLite function 'exfiltrate()' that simulates sending data
    to an attacker-controlled server (writes to a log file).
    """
    roll = request.args.get("roll", "") or request.form.get("roll", "")
    result = None
    debug_query = None
    exfil_log = None

    if roll:
        query = f"SELECT exfiltrate(name || ':' || password) FROM students WHERE roll_number = '{roll}'"
        debug_query = query

        conn = get_db()
        try:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            result = "Query executed. Check the exfiltration log below."
        except Exception as e:
            result = f"Error: {str(e)}"
        finally:
            conn.close()

    # Read exfiltration log
    if os.path.exists(OOB_LOG_PATH):
        with open(OOB_LOG_PATH, "r") as f:
            try:
                exfil_log = json.load(f)
            except:
                exfil_log = []

    return render_template("oob_demo.html", roll=roll, result=result, query=debug_query, exfil_log=exfil_log)


@app.route("/reset_db")
def reset_db():
    """Reset the database to initial state."""
    init_db()
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)

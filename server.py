import os
import sys

from flask import Flask, session, render_template, request,redirect, url_for, flash, make_response
from flask_session import Session
import psycopg2
from jinja2 import Environment, PackageLoader, select_autoescape
import csv
import json
import datetime

env = Environment(
    loader=PackageLoader('server', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

app = Flask(__name__)

db_conn = None
base_config = {}

def load_config(filename):
    with open(filename, "r") as config:
        return json.load(config)

# App Configurations / Settings
base_config = load_config("server.json")
app.logger.info("Connecting to postgres...")
# Connect to database
host = base_config["database"]["host"]
db = base_config["database"]["db"]
username = base_config["database"]["user"]
password = base_config["database"]["password"]
db_conn = psycopg2.connect(host=host, database=db,
                          user=username, password=password)
cur = db_conn.cursor()
bind_port = base_config["system"]["bind_port"]

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods = ["GET","POST"])
def login():#phi
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cur.execute("SELECT * FROM staff WHERE username = '{}' AND password = '{}'".format(username,password))
        x = cur.fetchone()
        if x is not None:
            session['d_id'] = x[0]
            session['name'] = x[1]
            session['admin'] = x[5]
            return redirect("/profile")
        else:
            flash("Wrong username or password")
            return redirect("/")


@app.route("/profile", methods = ["GET"])
def profile():#phi
    d_id = session['d_id']
    name = session['name']
    admin = session['admin']
    sql = """SELECT patient.p_id, patient.f_name, patient.l_name, patient.dob, patient.sex \
    FROM staff NATURAL JOIN patient_history INNER JOIN patient \
    ON patient_history.p_id = patient.p_id WHERE d_id = {} ORDER BY end_time;""".format(d_id)
    cur.execute(sql)
    patients = cur.fetchall()
    print(admin)
    if len(patients) > 5:
        patients = patients[:5]
    template = env.get_template('profile.html')
    return template.render(name = name, patients = patients, admin = admin)
@app.route("/search", methods = ["POST"])
def search():#phi
    query_type = request.form.get("query_type")
    info = request.form.get("search")
    sql = ""
    if query_type == "Patient Name":
        sql = "SELECT * FROM patient WHERE f_name LIKE '%{}%' OR l_name LIKE '%{}%';".format(info, info)
        cur.execute(sql)
        patients = cur.fetchall()
        template = env.get_template('patient_search_result.html')
        return template.render(patients = patients)
    elif query_type == "Patient ID":
        sql = "select * from patient"
        if bool(info.strip()):
            sql += " where p_id = {0}".format(info)
        cur.execute(sql)
        patients = cur.fetchall()
        template = env.get_template('patient_search_result.html')
        return template.render(patients = patients)
    elif query_type == "Staff Name":
        sql = "SELECT * FROM staff WHERE f_name LIKE '%{}%' OR l_name LIKE '%{}%';".format(info,info)
        cur.execute(sql)
        staff = cur.fetchall()
        print(staff, file = sys.stderr)
        template = env.get_template('search_result.html')
        return template.render(staffs = staff)
    elif query_type == "Staff ID":
        sql = "select * from staff"
        if bool(info.strip()):
            sql += " where s_id = {0}".format(info)
        cur.execute(sql)
        staff = cur.fetchall()
        print(staff, file = sys.stderr)
        template = env.get_template('search_result.html')
        return template.render(staffs = staff)
    template = env.get_template('search_result.html')
    return template.render()

@app.route("/createProcedure", methods = ["POST", "GET"])
def createProcedure():#jordan
    if request.method == "GET":
        template = env.get_template('createProcedure.html')
        return template.render()
    elif request.method == "POST":
        name = request.form.get("Procedure Name")
        cost = request.form.get("Cost")
        facility = request.form.get("Facility")
        per_hour = request.form.get("per_hour")
        cur.execute("INSERT into procedures (name, cost, facility, per_hour) VALUES (%s,%s,%s,%s)",(name, cost, facility, per_hour))
        db_conn.commit()
        return redirect("/")

@app.route("/addHistory/<p_id>", methods = ["GET"])
def addHistory(p_id):
    namesql = """SELECT f_name, l_name FROM patient WHERE p_id = {}""".format(p_id)
    cur.execute(namesql)
    names = cur.fetchone()
    procedure_sql = """SELECT pr_id, name FROM procedures;"""
    cur.execute(procedure_sql)
    procedure_names = cur.fetchall()
    med_sql = """SELECT m_id, name FROM medications""";
    cur.execute(med_sql)
    meds = cur.fetchall()
    print(meds, procedure_names, file = sys.stderr)
    template = env.get_template("addHistory.html")
    return template.render(name = names[0] + " " + names[1], p_id = p_id, \
                          procedure_names = procedure_names, medications = meds)

@app.route("/addProcedure/<p_id>", methods = ["POST"])
def addProcedure(p_id):
    s_id = session['d_id']
    pr_id = request.form.get("procedurename")
    description = request.form.get("description")
    start_date = request.form.get("start-date")
    end_date = request.form.get("end-date")
    sql = """INSERT INTO patient_history (pr_id, p_id, s_id, start_time, end_time, description) \
    VALUES (%s, %s, %s, %s, %s, %s)"""
    cur.execute(sql, [pr_id, p_id, s_id, start_date, end_date, description])
    db_conn.commit()
    return redirect("showBill/"+p_id)

@app.route("/addMedication/<p_id>", methods = ["POST"])
def addMedication(p_id):
    s_id = session['d_id']
    m_id = request.form.get("medications")
    dosage = request.form.get("dosage")
    today = datetime.datetime.now()
    hist_sql = """INSERT INTO patient_history (p_id, s_id, start_time, end_time) \
    VALUES (%s, %s, %s, %s)"""
    cur.execute(hist_sql, [p_id, s_id, today, today])
    db_conn.commit()
    tmp_sql = """SELECT MAX(ph_id) FROM patient_history;"""
    cur.execute(tmp_sql)
    max_id = cur.fetchone()[0]
    pres_sql = """INSERT INTO prescribed (ph_id, m_id, dosage) \
    VALUES (%s, %s, %s)"""
    cur.execute(pres_sql, (max_id, m_id, dosage))
    db_conn.commit()
    return redirect("showBill/"+p_id)

@app.route("/createPatient", methods = ["POST", "GET"])
def createPatient():#jordan
    if request.method == "GET":
        template = env.get_template('createPatient.html')
        return template.render()
    elif request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        age = request.form.get("age")
        dob = request.form.get("dob")
        address = request.form.get("address")
        phone = request.form.get("phone")
        sex = request.form.get("sex")
        height = request.form.get("height")
        weight = request.form.get("weight")
        cur.execute("""INSERT into patient (f_name, l_name, age, dob, address, phone_number, sex, height, weight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",(fname, lname, age, dob, address, phone, sex, height, weight))
        db_conn.commit()
        return redirect("/profile")

@app.route("/createStaff", methods = ["POST", "GET"])
def createStaff():#phi
    if request.method == "GET":
        sql = """SELECT * FROM hospital_department;"""
        cur.execute(sql)
        departments = cur.fetchall()
        template = env.get_template('createStaff.html')
        return template.render(departments = departments)
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        address = request.form.get("address")
        phone = request.form.get("phone")
        department = request.form.get("department_type")
        s_type = request.form.get("staff_type")
        dsql = "SELECT d_id FROM hospital_department WHERE dept_name = '{}'".format(department)
        cur.execute(dsql)
        d_id = cur.fetchone()[0]
        sql = """INSERT INTO staff (f_name, l_name, address, \
        phone_number, s_type, d_id, username, password) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        cur.execute(sql, (fname, lname, address, phone, s_type, d_id, username,password))
        db_conn.commit()
        return redirect("/profile")

@app.route("/staff/<s_id>", methods = ["GET", "POST"])
def staff(s_id):#ahsan
    sql = "SELECT * FROM staff WHERE s_id = {0};".format(s_id)
    cur.execute(sql)
    staff_sid = cur.fetchall()
    sqlUsers = "select p_id, f_name, l_name, pr_id, name, ph_id, start_time, end_time from (select ph_id from procedure_history where s_id = {0}) as selectedPH natural join patient_history natural join procedures natural join patient;".format(s_id)
    cur.execute(sqlUsers)
    patients = cur.fetchall()
    template = env.get_template('staff.html')
    return template.render(staff_sid = staff_sid, patients = patients)
    #return "<h1>{0}</h1>".format(s_id)

@app.route("/patient/<p_id>", methods = ["GET"])
def patient(p_id):#ahsan
    sql = "SELECT p_id, f_name, l_name, date_part('year', age(dob)) as age, dob, address, phone_number, sex, height, weight FROM patient WHERE p_id = {0};".format(p_id)
    cur.execute(sql)
    patient_sid = cur.fetchall()
    sqlProc = "select * from (select s_id, pr_id, start_time, end_time, description from patient_history where p_id = {0}) as selectedHist natural join (select s_id, concat(f_name, ' ', l_name) as staff_name from staff) as selectedStaff natural join (select pr_id, name as pr_name, facility from procedures) as selectedProc;".format(p_id)
    cur.execute(sqlProc)
    procedures = cur.fetchall()
    isActive_sql = """SELECT end_date FROM bills WHERE start_date = \
    (SELECT MAX(start_date) FROM bills WHERE p_id = {}) AND p_id = {};""".format(p_id, p_id)
    cur.execute(isActive_sql)
    x = cur.fetchone()
    if x[0] is None:
        isActive = True
    else:
        isActive = False
    print(x, file = sys.stderr)
    admin = session['admin']
    template = env.get_template('patient.html')
    return template.render(patient_sid = patient_sid, procedures = procedures, active = isActive, admin = admin)

@app.route("/startBill/<p_id>", methods = ["POST"])
def startBill(p_id):#phi
    sql = """INSERT INTO bills (p_id, start_date) VALUES (%s, %s)"""
    timenow = datetime.datetime.now()
    cur.execute(sql, [p_id, timenow])
    db_conn.commit()
    return redirect("/showBill/"+p_id)

@app.route("/showBill/<p_id>", methods = ["GET"])
def showBill(p_id):#phi
    med_sql = """SELECT name, purpose, dosage, s_id, description, end_time, cost \
    FROM medications NATURAL JOIN prescribed \
    NATURAL JOIN patient_history WHERE p_id = {} AND\
    start_time > (SELECT MAX(start_date) FROM bills \
    WHERE p_id = {})""".format(p_id, p_id)
    cur.execute(med_sql)
    meds = cur.fetchall()
    
    pr_sql = """SELECT name, facility, s_id, description, start_time, end_time, cost \
    FROM procedures NATURAL JOIN patient_history \
    WHERE p_id = {} AND start_time > (SELECT MAX(start_date) \
    FROM bills WHERE p_id = {});""".format(p_id, p_id)
    cur.execute(pr_sql)
    prs = cur.fetchall()
    p_sql = """SELECT f_name, l_name FROM patient WHERE p_id = {}""".format(p_id)
    cur.execute(p_sql)
    p_name = cur.fetchall()
    
    costs = calBill(p_id)
    isActive_sql = """SELECT end_date FROM bills WHERE start_date = \
    (SELECT MAX(start_date) FROM bills WHERE p_id = {}) AND p_id = {};""".format(p_id, p_id)
    cur.execute(isActive_sql)
    x = cur.fetchone()
    print(x, file = sys.stderr)
    if x[0] is None:
        isActive = True
    else:
        isActive = False
    template = env.get_template('genBill.html')
    return template.render(name = p_name[0][0]+" "+p_name[0][1], medications = meds,\
                           procedures = prs, cost = costs, p_id = p_id, active = isActive)
    

@app.route("/endBill/<p_id>", methods = ["POST"])
def endBill(p_id):#phi
    timenow = datetime.datetime.now()
    costs = calBill(p_id)
    update_sql = """UPDATE bills SET end_date = %s \
    WHERE start_date = (SELECT MAX(start_date) FROM bills \
    WHERE p_id = '{}')""".format(p_id)
    cur.execute(update_sql, [timenow])
    db_conn.commit()
    return '<html><body><h1>Transaction is complete!</h1></body></html>'
    
        
@app.route("/payBill/<p_id>", methods = ["POST"])
def payBill(p_id):#phi
    paid_str = request.form.get("pay")
    paid = 0
    try:
        paid = float(paid_str)
    except ValueError:
        print("not a number", file = sys.stderr)
        flash('Please enter an number')
    costs = calBill(p_id)
    print("Bill: ",paid, costs, file = sys.stderr)
    paid = paid +  float(costs[1]) 
    update_sql = """UPDATE bills SET total_paid = %s, total_cost = %s \
    WHERE start_date = (SELECT MAX(start_date) FROM bills \
    WHERE p_id = '{}')""".format( p_id)
    cur.execute(update_sql, [paid, costs[0]])
    db_conn.commit()
    return redirect("showBill/"+p_id)

def calBill(p_id):#phi
    bill_sql = """SELECT b_id FROM bills WHERE start_date = \
    (SELECT MAX(start_date) FROM bills WHERE p_id = {})""".format(p_id, p_id)
    cur.execute(bill_sql)
    bill_id = cur.fetchone()
    if bill_id[0] == 0:
        return [0,0,0]
    bill_id = bill_id[0]
    med_sql = """SELECT p_id, SUM(cost) FROM medications \
    NATURAL JOIN prescribed NATURAL JOIN patient_history \
    GROUP BY (p_id, start_time) HAVING p_id = {} AND start_time > \
    (SELECT max(start_date) FROM bills WHERE p_id = {});""".format(p_id, p_id)
    cur.execute(med_sql)
    med_cost = cur.fetchone()
    print(med_cost, file = sys.stderr)
    pr_sql = """SELECT p_id, sum(cost) FROM procedures NATURAL JOIN \
    patient_history GROUP BY (p_id, start_time) HAVING p_id = {} AND start_time > \
    (SELECT MAX(start_date) FROM bills WHERE p_id = {});""".format(p_id, p_id)
    cur.execute(pr_sql)
    pr_cost = cur.fetchone()
    if med_cost is None:
        med_cost = 0
    else:
        med_cost = med_cost[1]
    if pr_cost is None:
        pr_cost = 0
    else:
        pr_cost = pr_cost[1]
    total_cost = med_cost + pr_cost
    print(total_cost, file = sys.stderr)
    paid_sql = """SELECT total_paid FROM bills WHERE b_id = {}""".format(bill_id)
    cur.execute(paid_sql)
    total_paid = cur.fetchone()
    if total_paid[0] is None:
        total_paid = 0
    else:
        total_paid = total_paid[0]
    return [total_cost, total_paid, total_cost - total_paid] 

import os
import sys

from flask import Flask, session, render_template, request,redirect, url_for, flash, make_response
import psycopg2
from jinja2 import Environment, PackageLoader, select_autoescape
import csv
import json

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
# Session(app)


@app.route('/', methods = ["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cur.execute("SELECT * FROM staff WHERE username = '{}' AND password = '{}'".format(username,password))
        x = cur.fetchone()
        print(username, file= sys.stderr)
        if x is not None:
            return redirect("/profile")
        else:
            flash("Wrong username or password")
            return redirect("/")


@app.route("/profile", methods = ["GET"])
def profile():
    template = env.get_template('profile.html')
    return template.render()
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
        sql = "SELECT * FROM patient WHERE p_id = {}".format(info)
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
        sql = "SELECT * FROM staff WHERE s_id = {}".format(info)
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
    elif request.method == "POST":
        name = request.form.get("Procedure Name")
        cost = request.form.get("Cost")
        facility = request.form.get("Facility")
        per_hour = request.form.get("Per Hour?")
        cur.execute("INSERT into procedures (name, cost, facility, per_hour) VALUES (%s,%s,%s,%s)",(name, cost, facility, per_hour))
        db_conn.commit()
        return redirect("/")



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
        template = env.get_template('createStaff.html')
        return template.render()
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
        sql = """INSERT INTO staff (f_name, l_name, address, phone_number, s_type, d_id, username, password) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        cur.execute(sql, (fname, lname, address, phone, s_type, d_id, username,password))
        db_conn.commit()
        return redirect("/profile")

@app.route("/staff/<s_id>", methods = ["GET"])
def staff(s_id):#ahsan
    return

@app.route("/patient/<p_id>", methods = ["GET"])
def patient(p_id):#ahsan
    return

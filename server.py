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
        cur.execute("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username,password))
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
@app.route("/search", methods = ["GET"])
def search():
    query_type = request.form.get("query_type")
    info = request.form.get("search")
    sql = ""
    if query_type == "Patient Name":
        sql = "SELECT * FROM Patient WHERE f_name LIKE '%%{}%%' OR l_name LIKE '%%{}%%';".format(info, info)
        patients = cur.fetchall()
        template = env.get_template('search_result.html')
        return template.render(staffs = staff)
    elif query_type == "Patient ID":
        sql = "SELECT * FROM Patient WHERE p_id = {}".format(info)
        cur.execute(sql)
        patients = cur.fetchall()
        template = env.get_template('search_result.html')
        return template.render(staffs = staff)
    elif query_type == "Staff Name":
        sql = "SELECT * FROM Staff WHERE f_name LIKE '%%{}%%' OR l_name LIKE '%%{}%%';".format(info,info)
        cur.execute(sql)
        staff = cur.fetchall()
        template = env.get_template('search_result.html')
        return template.render(staffs = staff)
    elif query_type == "Staff ID":
        sql = "SELECT * FROM Staff WHERE s_id = {}".format(info)
        cur.execute(sql)
        staff = cur.fetchall()
        template = env.get_template('search_result.html')
        return template.render(staffs = staff)
    template = env.get_template('search_result.html')
    return template.render()
@app.route("/createProcedure", methods = ["POST", "GET"])
def createProcedure():
    if request.method == "GET":
        template = env.get_template('createProcedure.html')
        return template.render()


@app.route("/createPatient", methods = ["POST, GET"])
def createPatient():
    if request.method == "GET":
        template = env.get_template('createPatient.html')
        return template.render()

@app.route("/createStaff", methods = ["POST", "GET"])
def createStaff():
    return

@app.route("/staff/<s_id>", methods = ["GET"])
def staff(s_id):
    return

@app.route("/patient/<p_id>", methods = ["GET"])
def patient(p_id):
    return

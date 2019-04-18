import os
import sys

from flask import Flask, session, render_template, request,redirect, url_for, flash, make_response
import psycopg2
from jinja2 import Environment, PackageLoader, select_autoescape
import csv

env = Environment(
    loader=PackageLoader('server', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

app = Flask(__name__)

#Set the DATABASE_URL
DATABASE= "host = 'bowie.cs.earlham.edu' dbname = 'phnguyen17_db' user = 'phnguyen17'  password='abc.123'"
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

conn = psycopg2.connect(DATABASE)

@app.route('/', methods = ["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

@app.route("/profile", methods = ["GET"])
def profile():
    template = env.get_template('profile.html')
    return template.render()
@app.route("/search", methods = ["POST"])
def search():
    return

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

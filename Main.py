from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import desc
from flask import Blueprint, request, abort, jsonify, render_template
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv
import os
import ssl
import sys
from scripts import s_Today,s_Top

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# create database
DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'.format(**{
    'user': os.environ.get("DATABASE_USER"),
    'password': os.environ.get("DATABASE_PASSWORD"),
    'host': os.environ.get("DATABASE_HOST"),
    'port': 5432,
    'name': os.environ.get("DATABASE_NAME")
})

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain('server.crt', 'server.key')

db = SQLAlchemy(app)



class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    menu_type = db.Column(db.Integer, nullable = False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    menu_id = db.Column(db.Integer, nullable = False)
    sales_status = db.Column(db.Boolean, nullable = False, default=True)
    sold_time = db.Column(db.Time, nullable = False)
    date = db.Column(db.Date, nullable = False)

@app.route('/')
def title():
    return s_Top.main()

@app.route('/today')
def today():
    menu = Menu.query.all()
    schedule = Schedule.query.all()
    date = datetime.now()
    a = list(filter(lambda m: m.menu_type == 1 and m.date.month == date.month and m.date.day == date.day, menu))[0]
    b = list(filter(lambda m: m.menu_type == 2 and m.date.month == date.month and m.date.day == date.day, menu))[0]
    p = list(filter(lambda m: m.menu_type == 3 and m.date.month == date.month and m.date.day == date.day, menu))[0]
    
    return render_template("Today.html", menu = menu, schedule = schedule, a = a, b = b, p = p)


    #return s_Today.main()

if __name__== "__main__":
    app.run(debug=False, port=8084, threaded=True)
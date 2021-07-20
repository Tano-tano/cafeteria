from flask import Flask,render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import desc
from flask import Blueprint, request, abort, jsonify, render_template
import datetime as dt
from os.path import join, dirname
from dotenv import load_dotenv
import os
import ssl
import sys
from scripts import s_Today,s_Top
import psycopg2


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://team4:pianotileoraha@localhost:5432/team4db"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#load database
DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'.format(**{
    'user': os.environ.get("DATABASE_USER"),
    'password': os.environ.get("DATABASE_PASSWORD"),
    'host': os.environ.get("DATABASE_HOST"),
    'port': 5432,
    'name': os.environ.get("DATABASE_NAME")
})

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain('server.crt', 'server.key')

db = SQLAlchemy(app)



class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    menu_type = db.Column(db.Integer, nullable = False)
    sales_status = db.Column(db.Boolean, nullable = False, default=True)
    sold_time = db.Column(db.Time, nullable = False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, nullable = False)
    date = db.Column(db.Date, nullable = False)

#==================================当日メニュー取得===================================
def getToday():

    menu = Menu.query.all()
    #当日のAセットBセットを取得
    s = db.session.query(Schedule).filter(Schedule.date == dt.date.today()).all()


    #常設メニューの取得
    a_id, b_id = None, None
    if len(s) < 2:
        print("==================Schedule is None=======================")
    else:
        a_id, b_id = s[0].menu_id, s[1].menu_id
    #Aセットフィルター
    a = db.session.query(Menu)\
            .filter(Menu.menu_type == 1)\
            .filter(Menu.id == a_id)\
            .one_or_none()
    #Bセットフィルター
    b = db.session.query(Menu)\
            .filter(Menu.menu_type == 2)\
            .filter(Menu.id == b_id)\
            .one_or_none()
    #常設メニューフィルタ
    p = db.session.query(Menu)\
            .filter(Menu.menu_type == 3)\
            .all()


    return a,b,p,menu
#==================================================================================

#====================一週間のメニュー取得============================================
def getWeek():

    # menu = Menu.query.all()
    # a = list()
    # b = list()
    # days_array = ["月","火","水","木","金"]
    # days = dt.date.weekday(dt.datetime.strptime("2021/06/21","%Y/%m/%d"))

    # if days < 5:
    #     for i in range(5):
    #         theseDay = dt.datetime.strptime("2021/06/21","%Y/%m/%d") + dt.timedelta(days=i)
    #         #theseDay = dt.date.today() + dt.timedelta(days=i)

    #         s = db.session.query(Schedule).filter(Schedule.date + dt.timedelta(hours=0,minutes=0,seconds=0) == theseDay).all()


    #         a_id, b_id = s[0].menu_id, s[1].menu_id
    #         #Aセットフィルター
    #         a.append(db.session.query(Menu)\
    #                 .filter(Menu.menu_type == 1)\
    #                 .filter(Menu.id == a_id)\
    #                 .one_or_none())
    #         #Bセットフィルター
    #         b.append(db.session.query(Menu)\
    #                 .filter(Menu.menu_type == 2)\
    #                 .filter(Menu.id == b_id)\
    #                 .one_or_none())
    # return a,b,menu,days_array

    menu = Menu.query.all()
    a = list()
    b = list()
    days_array = ["月","火","水","木","金"]
    days_mmdd = [] # 日付(mm/dd)
    days = dt.date.weekday(dt.date.today())

    # 平日はその週を取得
    if days < 5:
        for i in range(5):
            theseDay = dt.date.today() - dt.timedelta(days=days-i)
            s = db.session.query(Schedule).filter(Schedule.date == theseDay).all()
            days_mmdd.append(str(theseDay.month) + "/" + str(theseDay.day))
            a_id, b_id = s[0].menu_id, s[1].menu_id
            #Aセットフィルター
            a.append(db.session.query(Menu)\
                .filter(Menu.menu_type == 1)\
                .filter(Menu.id == a_id)\
                .one_or_none())
            #Bセットフィルター
            b.append(db.session.query(Menu)\
                .filter(Menu.menu_type == 2)\
                .filter(Menu.id == b_id)\
                .one_or_none())

            
        
    # 土日は次の週を取得
    else:
        bias = 7 - days
        for i in range(5):
            theseDay = dt.date.today() + dt.timedelta(days=bias+i)
            s = db.session.query(Schedule).filter(Schedule.date == theseDay).all()
            days_mmdd.append(str(theseDay.month) + "/" + str(theseDay.day))

            a_id, b_id = s[0].menu_id, s[1].menu_id
            #Aセットフィルター
            a.append(db.session.query(Menu)\
                .filter(Menu.menu_type == 1)\
                .filter(Menu.id == a_id)\
                .one_or_none())
            #Bセットフィルター
            b.append(db.session.query(Menu)\
                .filter(Menu.menu_type == 2)\
                .filter(Menu.id == b_id)\
                .one_or_none())


    return a, b, menu, days_array, days_mmdd



#==================================================================================

@app.route('/')
def title():
    return s_Top.main()


@app.route('/today')
def today():
    ID = getToday()
    a, b, p, menu = ID[0], ID[1], ID[2], ID[3]
    return render_template("Today.html", menu = menu, a = a, b = b, p = p)


@app.route('/change/<id>')
def change(id):
    menu = Menu.query.get(id)
    return render_template("Change.html",menu = menu)


@app.route("/change/<id>/out_of_stock", methods=["POST"])
def out_of_stock(id):

    # avail_input_begin = dt.time(11, 30, 0)
    # avail_input_end = dt.time(13, 30, 0)
    nowtime = dt.datetime.now()
    now = nowtime.replace(microsecond=0)

    # 入力可能時間
    if (nowtime.hour == 11 and nowtime.minute >= 30) or (nowtime.hour == 12) or (nowtime.hour == 13 and nowtime.minute <= 30):

        menu = Menu.query.get(id)      
        if request.form['out_of_stock'] == "1":
            menu.sales_status = True                        
        else:
            menu.sales_status = False                      
            menu.sold_time = now
        db.session.add(menu)
        db.session.commit()                      
        
        return redirect("/today")
    # 入力可能時間外
    else:
        return redirect("/change/out_of_time")



@app.route('/week')
def weekly():
    ID = getWeek()
    a, b, menu, days, mmdd= ID[0], ID[1], ID[2], ID[3], ID[4]
    return render_template("Week.html",menu=menu, a=a, b=b, days=days, mmdd=mmdd)


@app.route('/change/out_of_time')
def out_of_tine():
    return render_template("Out_of_time.html")

    
if __name__== "__main__":
    app.run(host="172.16.16.7",port=8084)
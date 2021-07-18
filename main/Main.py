from flask import Flask
import c_TodayMenu

app = Flask(__name__)
@app.route('/')
def title():
    return ""

@app.route('/today')
def today_menu():
    return c_TodayMenu.main()

@app.route('/week')
def weekly_menu():
    return "week"

@app.route('/sale/change')    
def sales_change():
    return "change"

@app.route('/sale/time_out')
def time_out():
    return "time"

if __name__== "__main__":
    app.run(debug=True, port=8008, threaded=True)
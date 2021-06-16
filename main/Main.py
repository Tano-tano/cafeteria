from flask import Flask
app = Flask(__name__)
@app.route('/')
def title():
    return "title"

@app.route('/today')
def today_menu():
    return "today"

@app.route('/week')
def weekly_menu():
    return "week"

@app.route('/sale')
def sales_status():
    return "sale"

@app.route('/sale/change')    
def sales_change():
    return "change"

@app.route('/sale/time_out')
def time_out():
    return "time"

if __name__== "__main__":
    app.run(debug=True, port=8888, threaded=True)
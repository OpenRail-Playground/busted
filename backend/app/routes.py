# a simple page that says hello
from flask import current_app as app, render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/stations")
def get_stations():
    
    #stations = data.stations()
    #return jsonify(stations)
    return "Hello, stations"
import datetime
from flask import (current_app as app, Flask, render_template, jsonify, request)
from app.data import Data

data = Data()

@app.route('/')
def index():
    return render_template('index.html')   
    
@app.route("/agencies")
def get_agencies():
    agencies = data.agencies()
    return jsonify(agencies)

@app.route("/stations")
def get_stations():
    stations = data.stations()
    return jsonify(stations)

@app.route('/transfers/<int:stop_id>')
def get_transfers(stop_id):
    transfers = data.get_transfers_for_stop(stop_id)
    return jsonify(transfers)

@app.route('/arrivals/<int:stop_id>/', defaults={'date': None}, methods=['GET'])
@app.route('/arrivals/<int:stop_id>/<string:date>', methods=['GET'])
def get_arrivals(stop_id, date):
    if date is None:
        date = datetime.datetime.now().strftime('%Y%m%d')
    else:
        try:
            # Try to parse the date to ensure it's in the correct format
            date_obj = datetime.datetime.strptime(date, '%Y%m%d')
            # Reformat the date to ensure it's in the correct format
            date = date_obj.strftime('%Y%m%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYYMMDD."}), 400
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    arrivals = data.get_arrivals_for_stop(stop_id, date, start_time, end_time)
    return jsonify(arrivals)

@app.route('/connections/<int:stop_id>/', defaults={'date': None}, methods=['GET'])
@app.route('/connections/<int:stop_id>/<string:date>', methods=['GET'])
def get_connections(stop_id, date):
    if date is None:
        date = datetime.datetime.now().strftime('%Y%m%d')
    else:
        try:
            # Try to parse the date to ensure it's in the correct format
            date_obj = datetime.datetime.strptime(date, '%Y%m%d')
            # Reformat the date to ensure it's in the correct format
            date = date_obj.strftime('%Y%m%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYYMMDD."}), 400
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    connections = data.get_connections_for_stop(stop_id, date, start_time, end_time)
    return jsonify(connections)

@app.route('/arrival-conflicts/<int:stop_id>/', defaults={'date': None}, methods=['GET'])
@app.route('/arrival-conflicts/<int:stop_id>/<string:date>', methods=['GET'])
def get_arrival_conflicts(stop_id, date):
    if date is None:
        date = datetime.datetime.now().strftime('%Y%m%d')
    else:
        try:
            # Try to parse the date to ensure it's in the correct format
            date_obj = datetime.datetime.strptime(date, '%Y%m%d')
            # Reformat the date to ensure it's in the correct format
            date = date_obj.strftime('%Y%m%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYYMMDD."}), 400
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    connections = data.get_arrival_conflicts(stop_id, date, start_time, end_time)
    return jsonify(connections)

@app.route('/conflicts/<int:stop_id>/', defaults={'date': None}, methods=['GET'])
@app.route('/conflicts/<int:stop_id>/<string:date>', methods=['GET'])
def get_conflicts(stop_id, date):
    if date is None:
        date = datetime.datetime.now().strftime('%Y%m%d')
    else:
        try:
            # Try to parse the date to ensure it's in the correct format
            date_obj = datetime.datetime.strptime(date, '%Y%m%d')
            # Reformat the date to ensure it's in the correct format
            date = date_obj.strftime('%Y%m%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYYMMDD."}), 400
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    connections = data.get_conflicts(stop_id, date, start_time, end_time)
    return jsonify(connections)
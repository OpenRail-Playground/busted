import os
import db

from flask import (Flask, render_template, jsonify, request)
from data import Data

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'busted.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Set up the database handler
    db.init_app(app)
    
    data = Data()

    # a simple page that says hello
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
    
    @app.route('/arrivals/<int:stop_id>', methods=['GET'])
    def get_arrivals(stop_id):
        
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        arrivals = data.get_arrivals_for_stop(stop_id, start_time, end_time)
        return jsonify(arrivals)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
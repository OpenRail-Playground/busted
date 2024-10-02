import logging, os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_object('config.Config')
        #app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', handlers=[
        #logging.FileHandler("app.log"),
        logging.StreamHandler()
    ])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    #migrate = Migrate(app, db)

    with app.app_context():
        from . import routes
        from app.models import CurrentAgency, PreviousAgency, CurrentRoutes, PreviousRoutes, CurrentStops, PreviousStops, CurrentTrips, PreviousTrips, CurrentStopTimes, PreviousStopTimes, CurrentCalendar, PreviousCalendar, CurrentCalendarDates, PreviousCalendarDates, CurrentTransfers, PreviousTransfers
        # Initialize the database
        from .db_utils import init_db
        init_db()

    return app

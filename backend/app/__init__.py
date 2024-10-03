import logging, os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
   
    if test_config is None:
        app.config.from_object('config.Config')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', handlers=[logging.StreamHandler()])
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.init_app(app)

    with app.app_context():
        from . import routes
        # Initialize the database this takes quite a lot of time and is memory intensive depending on the amount of data in resources
        from .db_utils import init_db, extend_db
        init_db()
        extend_db()
    return app

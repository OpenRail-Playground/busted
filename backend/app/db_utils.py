import logging
import os
import csv
from sqlite3 import IntegrityError

from sqlalchemy import text
from app import create_app, db
from app.models import (
    CurrentAgency, PreviousAgency, CurrentRoutes, PreviousRoutes, 
    CurrentStops, PreviousStops, CurrentTrips, PreviousTrips, 
    CurrentStopTimes, PreviousStopTimes, CurrentCalendar, PreviousCalendar, 
    CurrentCalendarDates, PreviousCalendarDates, CurrentTransfers, PreviousTransfers)
    

def load_data(file_path, model):
    logging.info(f"Loading data from {file_path} into {model.__tablename__}")
    line = 1
    with open(file_path, newline='') as csvfile:
        #reader = csv.DictReader(csvfile)
        #data = [model(**row) for row in reader]
        #db.session.bulk_save_objects(data)
        reader = list(csv.DictReader(csvfile))  # Convert reader to a list to get the length
        total_rows = len(reader)
        data = []
        for index, row in enumerate(reader):
            data.append(model(**row))
            if (index + 1) % 10000 == 0:  # Log progress every 10000 rows
                logging.info(f'Processed {index + 1}/{total_rows} rows')
                db.session.bulk_save_objects(data)

def load_data_batch(file_path, model, batch_size=10000):
    logging.info(f"Loading data from {file_path} into {model.__tablename__}")
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for index, row in enumerate(reader):
            data.append(model(**row))
            if (index + 1) % batch_size == 0:
                latest_folder = os.path.basename(os.path.dirname(csvfile.name))
                filename = os.path.basename(csvfile.name)
                logging.info(f'Processed {index + 1} rows in {latest_folder}/{filename}')
                #logging.info(f'Processed {index + 1} rows in {csvfile.name}')
                try:
                    db.session.bulk_save_objects(data)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    logging.error("Integrity error occurred, rolling back.")
                data = []  # Clear the list for the next batch
        if data:  # Insert any remaining data
            try:
                db.session.bulk_save_objects(data)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                logging.error("Integrity error occurred, rolling back.")
    logging.info("Data loading completed.")

def init_db():
    logging.info(f"Initializing database")
    logging.info(f"Dropping all tables")
    db.drop_all()
    logging.info(f"Creating all tables")
    db.create_all()

    basedir = os.path.abspath(os.path.dirname(__file__))
    previous_data_dir = os.path.join(basedir, '../resources/data/previous')
    current_data_dir = os.path.join(basedir, '../resources/data/current')

    # Load data
    data_files = [
        ('agency.txt', CurrentAgency, PreviousAgency),
        ('calendar_dates.txt', CurrentCalendarDates, PreviousCalendarDates),
        ('calendar.txt', CurrentCalendar, PreviousCalendar),
        ('routes.txt', CurrentRoutes, PreviousRoutes),
        ('stop_times.txt', CurrentStopTimes, PreviousStopTimes),
        ('stops.txt', CurrentStops, PreviousStops),
        ('transfers.txt', CurrentTransfers, PreviousTransfers),
        ('trips.txt', CurrentTrips, PreviousTrips)
    ]

    logging.info(f"Loading data")
    for file_name, current_model, previous_model in data_files:
        load_data_batch(os.path.join(current_data_dir, file_name), current_model)
        load_data_batch(os.path.join(previous_data_dir, file_name), previous_model)
        db.session.commit()

    db.session.commit()
    logging.info(f"Finished db initialization")

def extend_db():
    logging.info(f"Updating db to extend dataset with qol data")

    with db.engine.connect() as conn:
        conn.execute(text("UPDATE current_stop_times SET stop_id_prefix = CAST(SUBSTR(stop_id, 1, 7) AS INTEGER)"))
        conn.execute(text("UPDATE previous_stop_times SET stop_id_prefix = CAST(SUBSTR(stop_id, 1, 7) AS INTEGER)"))

    logging.info(f"Creating additional indices")
    db.Index('idx_stop_times_stop_id_prefix', CurrentStopTimes.stop_id_prefix).create(db.engine)
    db.Index('idx_current_stop_times_stop_id', CurrentStopTimes.stop_id).create(db.engine)
    db.Index('idx_current_stop_times_trip_id', CurrentStopTimes.trip_id).create(db.engine)

    # Create indexes for previous_stop_times
    db.Index('idx_previous_stop_times_stop_id_prefix', PreviousStopTimes.stop_id_prefix).create(db.engine)
    db.Index('idx_previous_stop_times_stop_id', PreviousStopTimes.stop_id).create(db.engine)
    db.Index('idx_previous_stop_times_trip_id', PreviousStopTimes.trip_id).create(db.engine)

    # Create indexes for current tables
    db.Index('idx_current_trips_service_id', CurrentTrips.service_id).create(db.engine)
    db.Index('idx_current_calendar_service_id', CurrentCalendar.service_id).create(db.engine)
    db.Index('idx_current_calendar_dates_date', CurrentCalendarDates.date).create(db.engine)

    # Create indexes for previous tables
    db.Index('idx_previous_trips_service_id', PreviousTrips.service_id).create(db.engine)
    db.Index('idx_previous_calendar_service_id', PreviousCalendar.service_id).create(db.engine)
    db.Index('idx_previous_calendar_dates_date', PreviousCalendarDates.date).create(db.engine)


if __name__ == '__main__':
    #from app import create_app
    #app = create_app()
    #with app.app_context():
    init_db()
    extend_db()
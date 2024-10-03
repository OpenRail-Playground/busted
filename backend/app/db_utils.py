import logging
import os
import csv
from sqlite3 import IntegrityError
from sqlalchemy import text
from app import db
from app.models import (
    CurrentAgency, PreviousAgency, CurrentRoutes, PreviousRoutes, 
    CurrentStops, PreviousStops, CurrentTrips, PreviousTrips, 
    CurrentStopTimes, PreviousStopTimes, CurrentCalendar, PreviousCalendar, 
    CurrentCalendarDates, PreviousCalendarDates, CurrentTransfers, PreviousTransfers)
    
def load_data(file_path, model, batch_size=100000):
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
        load_data(os.path.join(current_data_dir, file_name), current_model)
        load_data(os.path.join(previous_data_dir, file_name), previous_model)
        db.session.commit()

    db.session.commit()
    logging.info(f"Finished db initialization")

def extend_db():
    logging.info(f"Updating db to extend dataset with qol data")
    db.session.execute(text("UPDATE current_stop_times SET stop_id_prefix = CAST(SUBSTR(stop_id, 1, 7) AS INTEGER)"))
    db.session.execute(text("UPDATE previous_stop_times SET stop_id_prefix = CAST(SUBSTR(stop_id, 1, 7) AS INTEGER)"))

    logging.info(f"Creating additional indices for current tables")
    db.session.execute(text("CREATE INDEX idx_stop_times_stop_id_prefix ON current_stop_times(stop_id_prefix)"))
    db.session.execute(text("CREATE INDEX idx_current_stop_times_stop_id ON current_stop_times(stop_id)"))
    db.session.execute(text("CREATE INDEX idx_current_stop_times_trip_id ON current_stop_times(trip_id)"))
    db.session.execute(text("CREATE INDEX idx_current_trips_service_id ON current_trips(service_id)"))
    db.session.execute(text("CREATE INDEX idx_current_calendar_service_id ON current_calendar(service_id)"))
    db.session.execute(text("CREATE INDEX idx_current_calendar_dates_date ON current_calendar_dates(date)"))

    # Create indexes for previous_stop_times
    logging.info(f"Creating additional indices for previous tables")
    db.session.execute(text("CREATE INDEX idx_previous_stop_times_stop_id_prefix ON previous_stop_times(stop_id_prefix)"))
    db.session.execute(text("CREATE INDEX idx_previous_stop_times_stop_id ON previous_stop_times(stop_id)"))
    db.session.execute(text("CREATE INDEX idx_previous_stop_times_trip_id ON previous_stop_times(trip_id)"))
    db.session.execute(text("CREATE INDEX idx_prevous_trips_service_id ON previous_trips(service_id)"))
    db.session.execute(text("CREATE INDEX idx_previous_calendar_service_id ON previous_calendar(service_id)"))
    db.session.execute(text("CREATE INDEX idx_previous_calendar_dates_date ON previous_calendar_dates(date)"))

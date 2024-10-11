#from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import foreign
from app import db

class BaseAgency(db.Model):
    __abstract__ = True  # This makes sure BaseModel is not created as a table
    agency_id = db.Column(db.String, primary_key=True)
    agency_name = db.Column(db.String, nullable=False)
    agency_url = db.Column(db.String, nullable=False)
    agency_timezone = db.Column(db.String, nullable=False)
    agency_lang = db.Column(db.String)
    agency_phone = db.Column(db.String)
    agency_fare_url = db.Column(db.String)
    agency_email = db.Column(db.String)

class CurrentAgency(BaseAgency):
    __tablename__ = 'current_agency'

class PreviousAgency(BaseAgency):
    __tablename__ = 'previous_agency'

class BaseStops(db.Model):
    __abstract__ = True  # This makes sure BaseModel is not created as a table
    stop_id = db.Column(db.String, primary_key=True)
    stop_code = db.Column(db.String)
    stop_name = db.Column(db.String, nullable=False)
    stop_desc = db.Column(db.String)
    stop_lat = db.Column(db.Float, nullable=False)
    stop_lon = db.Column(db.Float, nullable=False)
    zone_id = db.Column(db.String)
    stop_url = db.Column(db.String)
    location_type = db.Column(db.Integer)
    parent_station = db.Column(db.String, nullable=True)
    stop_timezone = db.Column(db.String)
    wheelchair_boarding = db.Column(db.Integer)


class CurrentStops(BaseStops):
    __tablename__ = 'current_stops'
    #parent_station = db.Column(db.String, db.ForeignKey('current_stops.stop_id'), nullable=True)
    @declared_attr
    def parent(cls):
        return db.relationship('CurrentStops', remote_side=[cls.stop_id],  primaryjoin=foreign(cls.parent_station) == cls.stop_id, backref='child_stops')


class PreviousStops(BaseStops):
    __tablename__ = 'previous_stops'
    #parent_station = db.Column(db.String, db.ForeignKey('previous_stops.stop_id'), nullable=True)
    @declared_attr
    def parent(cls):
        return db.relationship('PreviousStops', remote_side=[cls.stop_id], primaryjoin=foreign(cls.parent_station) == cls.stop_id, backref='child_stops')


class BaseRoutes(db.Model):
    __abstract__ = True  # This makes sure BaseModel is not created as a table
    route_id = db.Column(db.String, primary_key=True)
    agency_id = db.Column(db.String)
    route_short_name = db.Column(db.String, nullable=False)
    route_long_name = db.Column(db.String, nullable=False)
    route_desc = db.Column(db.String)
    route_type = db.Column(db.Integer, nullable=False)
    route_url = db.Column(db.String)
    route_color = db.Column(db.String)
    route_text_color = db.Column(db.String)

class CurrentRoutes(BaseRoutes):
    __tablename__ = 'current_routes'
    agency_id = db.Column(db.String, db.ForeignKey('current_agency.agency_id'))
    @declared_attr
    def parent(cls):
        return db.relationship('CurrentAgency', backref='routes')

class PreviousRoutes(BaseRoutes):
    __tablename__ = 'previous_routes'
    agency_id = db.Column(db.String, db.ForeignKey('previous_agency.agency_id'))
    @declared_attr
    def parent(cls):
        return db.relationship('PreviousAgency', backref='routes')

class BaseTrips(db.Model):
    __abstract__ = True  # This makes sure BaseModel is not created as a table
    trip_id = db.Column(db.String, primary_key=True)
    route_id = db.Column(db.String, nullable=False)
    service_id = db.Column(db.String, nullable=False)
    trip_headsign = db.Column(db.String)
    trip_short_name = db.Column(db.String)
    direction_id = db.Column(db.Integer)
    block_id = db.Column(db.String)
    shape_id = db.Column(db.String)
    wheelchair_accessible = db.Column(db.Integer)
    bikes_allowed = db.Column(db.Integer)

class CurrentTrips(BaseTrips):
    __tablename__ = 'current_trips'
    route_id = db.Column(db.String, db.ForeignKey('current_routes.route_id'))
    @declared_attr
    def parent(cls):
        return db.relationship('CurrentRoutes', backref='trips')

class PreviousTrips(BaseTrips):
    __tablename__ = 'previous_trips'
    route_id = db.Column(db.String, db.ForeignKey('previous_routes.route_id'))
    @declared_attr
    def parent(cls):
        return db.relationship('PreviousRoutes', backref='trips')

class BaseStopTimes(db.Model):
    __abstract__ = True  # This makes sure BaseModel is not created as a table
    trip_id = db.Column(db.String, primary_key=True)
    arrival_time = db.Column(db.String, nullable=False)
    departure_time = db.Column(db.String, nullable=False)
    stop_id = db.Column(db.String, primary_key=True)
    stop_sequence = db.Column(db.Integer, primary_key=True)
    stop_headsign = db.Column(db.String)
    pickup_type = db.Column(db.Integer)
    drop_off_type = db.Column(db.Integer)
    shape_dist_traveled = db.Column(db.Float)
    timepoint = db.Column(db.Integer)
    stop_id_prefix = db.Column(db.Integer)

class CurrentStopTimes(BaseStopTimes):
    __tablename__ = 'current_stop_times'
    trip_id = db.Column(db.String, db.ForeignKey('current_trips.trip_id'), primary_key=True)
    stop_id = db.Column(db.String, db.ForeignKey('current_stops.stop_id'), primary_key=True)
    @declared_attr
    def parent(cls):
        return db.relationship('CurrentTrips', backref='stop_times')
    @declared_attr
    def parent2(cls):
        return db.relationship('CurrentStops', backref='stop_times')

class PreviousStopTimes(BaseStopTimes):
    __tablename__ = 'previous_stop_times'
    trip_id = db.Column(db.String, db.ForeignKey('previous_trips.trip_id'), primary_key=True)
    stop_id = db.Column(db.String, db.ForeignKey('previous_stops.stop_id'), primary_key=True)
    @declared_attr
    def parent(cls):
        return db.relationship('PreviousTrips', backref='stop_times')
    @declared_attr
    def parent2(cls):
        return db.relationship('PreviousStops', backref='stop_times')

class BaseCalendar(db.Model):
    __abstract__ = True  # This makes sure BaseModel is not created as a table
    service_id = db.Column(db.String, primary_key=True)
    monday = db.Column(db.Integer, nullable=False)
    tuesday = db.Column(db.Integer, nullable=False)
    wednesday = db.Column(db.Integer, nullable=False)
    thursday = db.Column(db.Integer, nullable=False)
    friday = db.Column(db.Integer, nullable=False)
    saturday = db.Column(db.Integer, nullable=False)
    sunday = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)

class CurrentCalendar(BaseCalendar):
    __tablename__ = 'current_calendar'

class PreviousCalendar(BaseCalendar):
    __tablename__ = 'previous_calendar'

class BaseCalendarDates(db.Model):
    __abstract__ = True  # This makes sure BaseModel is not created as a table
    service_id = db.Column(db.String, primary_key=True)
    date = db.Column(db.String, primary_key=True)
    exception_type = db.Column(db.Integer, nullable=False)

class CurrentCalendarDates(BaseCalendarDates):
    __tablename__ = 'current_calendar_dates'
    service_id = db.Column(db.String, db.ForeignKey('current_calendar.service_id'), primary_key=True)
    @declared_attr
    def parent(cls):
        return db.relationship('CurrentCalendar', backref='calendar_dates')

class PreviousCalendarDates(BaseCalendarDates):
    __tablename__ = 'previous_calendar_dates'
    service_id = db.Column(db.String, db.ForeignKey('previous_calendar.service_id'), primary_key=True)
    @declared_attr
    def parent(cls):
        return db.relationship('PreviousCalendar', backref='calendar_dates')

class BaseTransfers(db.Model):
    __abstract__ = True  # This makes sure BaseModel is not created as a table
    from_stop_id = db.Column(db.String, primary_key=True)
    to_stop_id = db.Column(db.String, primary_key=True)
    transfer_type = db.Column(db.Integer, nullable=False)
    min_transfer_time = db.Column(db.Integer)

class CurrentTransfers(BaseTransfers):
    __tablename__ = 'current_transfers'
    from_stop_id = db.Column(db.String, db.ForeignKey('current_stops.stop_id'), primary_key=True)
    to_stop_id = db.Column(db.String, db.ForeignKey('current_stops.stop_id'), primary_key=True)
    @declared_attr
    def FromStop(cls):
        return db.relationship('CurrentStops', foreign_keys=[cls.from_stop_id], backref='current_transfers_from')
    
    @declared_attr
    def ToStop(cls):
        return db.relationship('CurrentStops', foreign_keys=[cls.to_stop_id], backref='current_transfers_to')


class PreviousTransfers(BaseTransfers):
    __tablename__ = 'previous_transfers'
    from_stop_id = db.Column(db.String, db.ForeignKey('previous_stops.stop_id'), primary_key=True)
    to_stop_id = db.Column(db.String, db.ForeignKey('previous_stops.stop_id'), primary_key=True)
    @declared_attr
    def FromStop(cls):
        return db.relationship('PreviousStops', foreign_keys=[cls.from_stop_id], backref='previous_transfers_from')
    
    @declared_attr
    def ToStop(cls):
        return db.relationship('PreviousStops', foreign_keys=[cls.to_stop_id], backref='previous_transfers_to')

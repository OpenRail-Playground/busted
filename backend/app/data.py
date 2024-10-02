from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import text
#from app import db

db = SQLAlchemy()

PREVIOUS = "previous_"
CURRENT = "current_"
TRANSFER_TIME = 29

class Data():
    
    def __init__(self,):
        pass

    def stations(self, table_prefix=CURRENT):
        query = f'SELECT * FROM {table_prefix}stops'
        stations = db.session.execute(query).fetchall()
        return stations
    
    def agencies(self, table_prefix=CURRENT):
        query = f'SELECT agency_id as id, agency_name FROM {table_prefix}agency ORDER BY agency_name ASC'
        agencies = db.session.execute(query).fetchall()
        agencies_list = [dict(row) for row in agencies]
        return agencies_list
    
    def get_transfers_for_stop(self, stop_id, table_prefix=CURRENT):
        # Use LIKE to match stop_id with potential suffixes
        stop_id_like = f"{stop_id}%"
        
        query = text(f'''
        SELECT 
            from_stop_id AS original_stop_id,
            to_stop_id AS transfer_stop_id,
            min_transfer_time
        FROM {table_prefix}transfers
        WHERE from_stop_id LIKE ?
        ''')
        
        results = db.session.execute(query, (stop_id_like,)).fetchall()
                
        # Clean and consolidate results in Python
        transfers = {}
        for row in results:
            connected_stop_id = row['transfer_stop_id']
            min_transfer_time = row['min_transfer_time']
            
            # Extract the base stop_id (before any suffix)
            base_stop_id = connected_stop_id.split(':')[0]
            
            # Update the dictionary with the maximum transfer time for each base stop_id
            if base_stop_id not in transfers or min_transfer_time > transfers[base_stop_id]:
                transfers[base_stop_id] = min_transfer_time
                
        # Remove the original stop_id from the results
        if stop_id in transfers:
            del transfers[stop_id]
        
        return transfers
    
    def get_day_of_week_column(self, date):
        date_obj = datetime.strptime(date, '%Y%m%d')
        weekday = date_obj.weekday()
        return ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][weekday]
    
    # the actual function, but it's too slow for demo and needs optimizations
    def get_stop_times(self, stop_id, date, start_time, end_time, time_column, table_prefix=CURRENT):
        weekday_column = self.get_day_of_week_column(date)
        query = text(f'''
        SELECT 
            st.trip_id as trip_id, 
            st.arrival_time as arrival_time, 
            st.departure_time as departure_time, 
            t.route_id,
            t.service_id,
            t.trip_headsign as headsign,
            t.trip_short_name as short_name,
            t.direction_id as direction
        FROM {table_prefix}stop_times st
        JOIN {table_prefix}trips t ON st.trip_id = t.trip_id
        JOIN {table_prefix}calendar c ON t.service_id = c.service_id
        LEFT JOIN {table_prefix}calendar_dates pcd ON t.service_id = pcd.service_id AND pcd.date = ?
        WHERE st.stop_id_prefix = ?
        AND st.{time_column} BETWEEN ? AND ?
        AND c.{weekday_column} = 1
        AND c.start_date <= ?
        AND c.end_date >= ?
        AND (pcd.exception_type IS NULL OR pcd.exception_type = 1)
        ORDER BY st.{time_column}
        ''')
        results = db.session.execute(query, (date, stop_id, start_time, end_time, date, date)).fetchall()
        return [dict(row) for row in results]
    
    # a mocked version of the function, that trivialises by filtering by short_name
    def mocked_get_stop_times(self, stop_id, date, start_time, end_time, time_column, table_prefix=CURRENT):       
        query = text(f'''
        SELECT 
            st.trip_id as trip_id, 
            st.arrival_time as arrival_time, 
            st.departure_time as departure_time, 
            t.route_id,
            t.service_id,
            t.trip_headsign as headsign,
            t.trip_short_name as short_name,
            t.direction_id as direction
        FROM {table_prefix}stop_times st
        JOIN {table_prefix}trips t ON st.trip_id = t.trip_id
        WHERE st.stop_id_prefix = ?
        AND st.{time_column} BETWEEN ? AND ?
        ORDER BY st.{time_column}
        ''')
        
        results = db.session.execute(query, (stop_id, start_time, end_time)).fetchall()
        
        # Konvertieren Sie die Ergebnisse in eine Liste von Dictionaries
        result_dicts = [dict(row) for row in results]
    
        return self.filter_stop_times(result_dicts, date)
    
    #used to filter the stop times in the mocked function
    def filter_stop_times(self, stop_times, date):
        
        unique_short_names = set()
        filtered_stop_times = []
        
        for stop_time in stop_times:
            short_name = stop_time['short_name']
            
            if short_name not in unique_short_names:
                unique_short_names.add(short_name)
                filtered_stop_times.append(stop_time)
        
        return filtered_stop_times

    def get_arrivals_for_stop(self, stop_id, date, start_time, end_time, table_prefix=CURRENT):
        # TODO replace with a non mocked version
        return self.mocked_get_stop_times(stop_id, date, start_time, end_time, 'arrival_time', table_prefix)
    
    def get_departures_for_stop(self, stop_id, date, start_time, end_time, table_prefix=CURRENT):
        # TODO replace with a non mocked version
        return self.mocked_get_stop_times(stop_id, date, start_time, end_time, 'departure_time', table_prefix)

    def get_arrival_conflicts(self, stop_id, date, start_time, end_time):
        previous_arrivals = self.get_arrivals_for_stop(stop_id, date, start_time, end_time, PREVIOUS)
        
        current_end_time_limit = (datetime.strptime(end_time, '%H:%M:%S') + timedelta(minutes=TRANSFER_TIME)).time().strftime('%H:%M:%S')
        current_arrivals = self.get_arrivals_for_stop(stop_id, date, start_time, current_end_time_limit, CURRENT)
        
        differences = {}
        
        # Index current_arrivals by short_name for quick lookup
        current_arrivals_dict = {arrival['short_name']: arrival for arrival in current_arrivals}
            
        for previous_trip in previous_arrivals:
            short_name = previous_trip['short_name']
            previous_arrival_time = previous_trip['arrival_time']
            current_trip = current_arrivals_dict.get(short_name)
    
            if current_trip:
                current_arrival_time = current_trip['arrival_time']
                
                if previous_arrival_time != current_arrival_time:
                    # Es gibt eine Änderung in der Ankunftszeit
                    conflict_connections = self.get_conflict_connections(stop_id, date, previous_arrival_time, current_arrival_time)
                    
                    differences[short_name] = {
                        'old_arrival_time': previous_arrival_time,
                        'new_arrival_time': current_arrival_time,
                        'conflicts': conflict_connections
                    }
    
        return differences        
    
    def get_conflict_connections(self, stop_id, date, previous_arrival_time, new_arrival_time):
       
        conflicts = []
       
        transfers = self.get_transfers_for_stop(stop_id)
       
        for transfer_stop_id, min_transfer_time in transfers.items():
            min_transfer_time_minutes = int(min_transfer_time) // 60
    
            transfer_start_time = (datetime.strptime(previous_arrival_time, '%H:%M:%S') + timedelta(minutes=min_transfer_time_minutes)).time().strftime('%H:%M:%S')
            transfer_end_time = (datetime.strptime(new_arrival_time, '%H:%M:%S') + timedelta(minutes=min_transfer_time_minutes)).time().strftime('%H:%M:%S')
    
            departures = self.get_departures_for_stop(transfer_stop_id, date, transfer_start_time, transfer_end_time)
    
            for departure in departures:
                departure['transfer_stop_id'] = transfer_stop_id  # Fügen Sie den transfer_stop_id zur Verbindung hinzu
                conflicts.append(departure)
    
        return conflicts
        
    def get_connections_for_stop(self, stop_id, date, start_time, end_time, table_prefix=CURRENT):    
        # Schritt 1: Alle Ankünfte am gegebenen Stop abfragen
        arrivals = self.get_arrivals_for_stop(stop_id, date, start_time, end_time, table_prefix)
        
        trips = {}
    
        for arrival in arrivals:
            arrival_time = arrival['arrival_time']
            short_name = arrival['short_name']
    
            # Schritt 2: Alle Transfer-Haltestellen für den gegebenen Stop abfragen
            transfers = self.get_transfers_for_stop(stop_id, table_prefix)
    
            trips[short_name] = {
                'arrival_time': arrival_time,
                'connections': []
            }
    
            # Schritt 3: Für jede Transfer-Haltestelle die Abfahrten innerhalb des Transferfensters abfragen
            for transfer_stop_id, min_transfer_time in transfers.items():
                min_transfer_time_minutes = int(min_transfer_time) // 60
                
                transfer_start_time = (datetime.strptime(arrival_time, '%H:%M:%S') + timedelta(minutes=min_transfer_time_minutes)).time().strftime('%H:%M:%S')
                transfer_end_time = (datetime.strptime(arrival_time, '%H:%M:%S') + timedelta(minutes=TRANSFER_TIME)).time().strftime('%H:%M:%S')
    
                departures = self.get_departures_for_stop(transfer_stop_id, date, transfer_start_time, transfer_end_time, table_prefix)
                for departure in departures:
                    departure['transfer_stop_id'] = transfer_stop_id  # Fügen Sie den transfer_stop_id zur Verbindung hinzu
                    trips[short_name]['connections'].append(departure)
    
        return trips
    
    def get_conflicts(self, stop_id, date, start_time, end_time):
        previous_connections = self.get_connections_for_stop(stop_id, date, start_time, end_time, PREVIOUS)
        
        current_end_time_limit = datetime.strptime(end_time, '%H:%M:%S') + timedelta(minutes=TRANSFER_TIME)
        current_connections = self.get_connections_for_stop(stop_id, date, start_time, current_end_time_limit, CURRENT)
        
        differences = {}
            
        for short_name, previous_trip in previous_connections.items():
            previous_arrival_time = previous_trip['arrival_time']
            current_trip = current_connections.get(short_name)
    
            if current_trip:
                current_arrival_time = current_trip['arrival_time']
                
                if previous_arrival_time != current_arrival_time:
                    # Es gibt eine Änderung in der Ankunftszeit
                    differences[short_name] = {
                        'old_arrival_time': previous_arrival_time,
                        'new_arrival_time': current_arrival_time,
                        'conflicts': []
                    }

                    # Prüfen, ob Verbindungen verloren gehen
                    previous_connections_set = {(c['trip_id'], c['transfer_stop_id']) for c in previous_trip['connections']}
                    current_connections_set = {(c['trip_id'], c['transfer_stop_id']) for c in current_trip['connections']}
                    
                    conflicts = previous_connections_set - current_connections_set
                    
                    for trip_id, transfer_stop_id in conflicts:
                        for connection in previous_trip['connections']:
                            if connection['trip_id'] == trip_id and connection['transfer_stop_id'] == transfer_stop_id:
                                differences[short_name]['conflicts'].append(connection)
                                break
    
        return differences

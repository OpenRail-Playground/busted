from db import get_db


class Data():
    
    def __init__(self,):
        pass

    def stations(self,):
        db = get_db()

        stations = db.execute('SELECT * FROM stops').fetchall()
        
        return stations
    
    def agencies(self,):
        db = get_db()

        agencies = db.execute('SELECT agency_id as id, agency_name FROM current_agency ORDER BY agency_name ASC').fetchall()
        
        agencies_list = [dict(row) for row in agencies]
        
        return agencies_list
    
    def get_transfers_for_stop(self, stop_id):
        db = get_db()
        
        # SQL query to find all connections for the given stop_id
        query = '''
        SELECT 
            CASE 
                WHEN from_stop_id = ? THEN to_stop_id 
                ELSE from_stop_id 
            END AS connected_stop_id,
            min_transfer_time
        FROM current_transfers
        WHERE from_stop_id = ? OR to_stop_id = ?
        '''
        
        results = db.execute(query, (stop_id, stop_id, stop_id)).fetchall()
        
        # Convert to the desired data structure
        transfers = {}
        for row in results:
            connected_stop_id = row['connected_stop_id']
            min_transfer_time = row['min_transfer_time']
            if connected_stop_id not in transfers:
                transfers[connected_stop_id] = min_transfer_time
        
        return transfers
    
    def get_arrivals_for_stop(self, stop_id, start_time, end_time):
        db = get_db()
        
        # SQL query to find all arrivals for the given stop_id and time window
        query = '''
        SELECT trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type, drop_off_type
        FROM previous_stop_times
        WHERE stop_id = ?
        AND arrival_time BETWEEN ? AND ?
        '''
        
        results = db.execute(query, (stop_id, start_time, end_time)).fetchall()
        
        # Convert the rows to dictionaries
        arrivals = [dict(row) for row in results]
        
        return arrivals
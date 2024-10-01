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

        agencies = db.exectue('SELECT * FROM current_agency')
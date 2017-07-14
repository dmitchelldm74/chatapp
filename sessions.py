from datetime import datetime, timedelta
import sqlite3


class Session():
    def __init__(self, connection, cursor):
        self.conn = connection 
        self.cur = cursor
        
    def new(self, key, user="null"):
        now = datetime.now()
        self.cur.execute('INSERT INTO sessions VALUES (?,?,?,?)',(key, str(now),str(now+timedelta(minutes=15.1)), user))
        self.conn.commit()
        
    def get(self, key):
        return self.cur.execute('SELECT * FROM sessions WHERE key=?', (key,)).fetchone()
        
    def checkexpiration(self, key):
        session = list(self.get(key))
        if session != None:
            if datetime.now() >= datetime.strptime(session[2],"%Y-%m-%d %H:%M:%S.%f"):
                return False
        return True
        

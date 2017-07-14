import uuid, sqlite3
from sessions import Session, datetime
import hashlib

class fake_response():
    headers = {}
    def __init__(self):
        self.fake = True
    
    def set_cookie(self, key, value):
        return None
        

class AUTH():
    def __init__(self, response):
        self.__key = str(uuid.uuid4())
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.response = response
        self.session = Session(self.connection,self.cursor)
        
    def login(self, user, password):
        password = self.hashps(password)
        if self.cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (user, password)):
            self.credentials = (self.__key, user, password)
            self.response.set_cookie('AUTH', self.__key)
            self.response.headers['Refresh'] = '1'
            self.session.new(self.__key, user)
            return "true"
        else:
            self.response.set_cookie('AUTH', 'None')
            return "false"
        
    def new(self, user, password):
        if self.cursor.execute('SELECT id FROM users WHERE username=?',(user,)).fetchone() == None:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?,?)',(user, self.hashps(password)))
            self.connection.commit()
            return True
        return False
        
    def hashps(self,password):
        return hashlib.sha256(password).hexdigest()
        
    def close(self):
        self.connection.close()
        
class KEY_AUTH():
    _logout = False
    def __init__(self, key, response=fake_response()):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.key = key
        self.response = response
        self.session = Session(self.connection,self.cursor)
        self.credentials = (self.key, self.session.get(self.key)[3])
        
    def login(self):
        if self.session.checkexpiration(self.key) == False or self._logout == True:
            self.response.set_cookie('AUTH', 'None')
            self.cursor.execute('UPDATE sessions SET expiration=? WHERE key=?',(str(datetime.now()),self.key))
            self.connection.commit()
            self.response.headers['Refresh'] = '1'
            return False
        return True
        
    def logout(self):
        self._logout = True       
        
    def close(self):
        self.connection.close()
        
def SEND_MESSAGE(auth, To, data):
    if auth.login() == True and To != "" and data != "" and auth.cursor.execute('SELECT * FROM users WHERE username=?',(To,)).fetchone() != None:
        username = auth.credentials[1]
        auth.cursor.execute('INSERT INTO messages (_from, _to, content, timestamp) VALUES (?,?,?,?)', (username, To, data, str(datetime.now())))
        auth.connection.commit()
        auth.response.headers['Refresh'] = '1'
        return True
    else:
        return False
        
def GET_MESSAGES(auth):
    if auth.login() == True:
        messages = list(auth.cursor.execute('SELECT * FROM messages WHERE _to=? ORDER BY timestamp DESC',(auth.credentials[1],)).fetchall())
        if len(messages) >= 6:
            auth.cursor.execute('DELETE FROM messages WHERE _to=? ORDER BY timestamp LIMIT 5',(auth.credentials[1],))
            auth.connection.commit()
        return messages
    return []
    
def LOG(auth):
    if auth.login() == True:
        username = auth.credentials[1]
        json = {"owner":username}
        data = list(auth.cursor.execute('SELECT * FROM sessions WHERE user=?',(username,)).fetchall())
        i = 0
        for d in data:
            json[i] = {"login":d[1], "logout":d[2]}
            i += 1
        return str(json)
    return "{}"
        
        
        

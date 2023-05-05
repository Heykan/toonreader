from app import database

class User():
    def __init__(self, id, username, password, email, mod = 0, avatar = ""):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.mod = mod
        self.avatar = avatar

class UserModel:
    #@app.context_processor
    def __init__(self):
        self.conn = database.get_db()

    def add_user(self, user):
        query = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        self.conn.execute(query, (user.username, user.password, user.email))
        self.conn.commit()

    def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username = ?"
        result = self.conn.execute(query, (username,))
        row = result.fetchone()
        if row is None:
            return None
        
        return User(*row[:6])
    
    def get_user_by_id(self, id):
        query = "SELECT * FROM users WHERE id = ?"
        result = self.conn.execute(query, (id,))
        row = result.fetchone()
        if row is None:
            return None
        
        return User(*row[:6])
    
    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email = ?"
        result = self.conn.execute(query, (email,))
        row = result.fetchone()
        if row is None:
            return None
        
        return User(*row[:6])

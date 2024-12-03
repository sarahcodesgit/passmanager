import sqlite3

class DatabaseManager:
    def __init__(self, db_name="passwords.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_password(self, service, username, password):
        query = "INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)"
        self.conn.execute(query, (service, username, password))
        self.conn.commit()

    def get_password(self, service):
        query = "SELECT username, password FROM passwords WHERE service = ?"
        return self.conn.execute(query, (service,)).fetchone()
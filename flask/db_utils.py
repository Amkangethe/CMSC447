# db_utils.py

import sqlite3
from flask_login import UserMixin

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

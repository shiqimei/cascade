import sqlite3
from sqlite3 import Error

def create_connection():
    try:
        conn = sqlite3.connect('database.db')
        return conn
    except Error as e:
        print(e)

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE users (
                          userid TEXT PRIMARY KEY,
                          username TEXT,
                          github_access_token TEXT
                          )""")
    except Error as e:
        print(e)

def insert_default_user(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (userid, username) VALUES ('shiqimei', 'Shiqi Mei')")
        conn.commit()
    except Error as e:
        print(e)

def update_access_token(conn, userid, token):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET github_access_token = ? WHERE userid = ?", (token, userid))
        conn.commit()
    except Error as e:
        print(e)

def query_user(conn, userid):
    """Query a user from the database by userid."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE userid = ?", (userid,))
        user = cursor.fetchone()
        return user
    except Error as e:
        print(e)
        return None

def init_database():
    """Initializes the database."""
    conn = create_connection()
    create_table(conn)
    insert_default_user(conn)
    return conn
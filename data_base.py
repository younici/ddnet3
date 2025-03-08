import sqlite3, os

if not os.path.exists('DataBase'):
    os.makedirs('Database')

with sqlite3.connect('DataBase/Users.db') as db:
    cursor = db.cursor()
    query = """ CREATE TABLE IF NOT EXISTS users(local_id INTEGER, tt_username TEXT, id INTEGER, username TEXT, name TEXT) """
    cursor.execute(query)

def insert_user(local_id, id, username, name, tt_username):
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = """INSERT INTO users (local_id, id, username, name, tt_username) VALUES(?, ?, ?, ?, ?)"""
        cursor.execute(query, (local_id, id, username, name, tt_username))

def set_ttname(id, tt_username):
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = """UPDATE users SET tt_username = ? WHERE id = ?"""
        cursor.execute(query, (tt_username, id))

def set_fullname(id, username, name):
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = """UPDATE users SET username = ?, name = ? WHERE id = ?"""
        cursor.execute(query, (username, name, id))

def get_user(id):
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = f"""SELECT local_id, id, username, name, tt_username, FROM users WHERE id = ?"""
        cursor.execute(query, (id,))
        return cursor.fetchone()

def get_username(id):
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = f"""SELECT username FROM users WHERE id = ?"""
        cursor.execute(query, (id,))
        return cursor.fetchone()[0]

def get_user_tt_username(id):
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = f"""SELECT name FROM users WHERE id = ?"""
        cursor.execute(query, (id,))
        return cursor.fetchone()[0]

def del_user(id):
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = """DELETE FROM users WHERE id = ?"""
        cursor.execute(query, (id,))

def del_user_local_id(local_id):
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = """DELETE FROM users WHERE local_id = ?"""
        cursor.execute(query, (local_id,))

def user_count():
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = """SELECT COUNT(*) FROM users"""
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]
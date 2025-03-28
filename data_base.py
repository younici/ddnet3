import sqlite3

with sqlite3.connect('DataBase/Users.db') as db:
    cursor = db.cursor()
    query = """ CREATE TABLE IF NOT EXISTS users(local_id INTEGER, id INTEGER, name TEXT, username TEXT, tt_username TEXT) """
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
        query = f"""SELECT local_id, id, username, name, tt_username FROM users WHERE id = ?"""
        cursor.execute(query, (id,))
        return cursor.fetchone()

def get_user_by_local_id(local_id):
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = f"""SELECT local_id, id, username, name, tt_username FROM users WHERE local_id = ?"""
        cursor.execute(query, (local_id,))
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
        query = f"""SELECT tt_username FROM users WHERE id = ?"""
        cursor.execute(query, (id,))
        return cursor.fetchone()[0]

def get_by_tt_username(tt_username):
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = f"""SELECT local_id, id, username, name, tt_username FROM users WHERE tt_username = ?"""
        cursor.execute(query, (tt_username,))
        return cursor.fetchone()

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

def search_users_by_word(word):
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = """SELECT DISTINCT * FROM users WHERE tt_username LIKE ?"""
        cursor.execute(query, (f"%{word}%",))
        return cursor.fetchall()

def user_count():
    with sqlite3.connect('DataBase/Users.db') as db:
        cursor = db.cursor()
        query = """SELECT COUNT(*) FROM users"""
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]
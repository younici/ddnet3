import sqlite3
import datetime

pathDB = 'Database/data.db'
with sqlite3.connect(pathDB) as db:
    cursor = db.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users(local_id INTEGER, id INTEGER, name TEXT, username TEXT, tt_username TEXT) """)
    cursor.execute(""" CREATE TABLE IF NOT EXISTS params(updMessage INTEGER, commandCooldown INTEGER, updMessageText TEXT) """)
    cursor.execute("SELECT COUNT(*) FROM params")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""INSERT INTO params(updMessage, commandCooldown, updMessageText) VALUES(1, 30, 'база данных обновлена!')""")
    cursor.execute(""" CREATE TABLE IF NOT EXISTS "last use time command"(id INTEGER, time TEXT) """)
    db.commit()

def insert_user(local_id, id, username, name, tt_username):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""INSERT INTO users (local_id, id, username, name, tt_username) VALUES(?, ?, ?, ?, ?)""", (local_id, id, username, name, tt_username))
        db.commit()

def set_local_id(id, local_id):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""UPDATE users SET local_id = ? WHERE id = ?""", (local_id, id))
        db.commit()

def set_ttname(id, tt_username):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""UPDATE users SET tt_username = ? WHERE id = ?""", (tt_username, id))
        db.commit()

def set_fullname(id, username, name):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""UPDATE users SET username = ?, name = ? WHERE id = ?""", (username, name, id))
        db.commit()

def set_upd_message_status(status):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""UPDATE params SET updMessage = ?""", (status,))
        db.commit()

def set_upd_message_text(text):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""UPDATE params SET updMessageText = ?""", (text,))
        db.commit()

def set_command_cooldown(seconds):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""UPDATE params SET commandCooldown = ?""", (seconds,))
        db.commit()

def set_user_last_time_use_command(id, time):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        if cursor.execute("""SELECT * FROM "last use time command" WHERE id = ?""", (id,)).fetchone() is None:
            cursor.execute("""INSERT INTO "last use time command" (id, time) VALUES(?, ?)""", (id, time))
        else:
            cursor.execute("""UPDATE "last use time command" SET time = ? WHERE id = ?""", (time, id))
        db.commit()

def get_all_users():
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT local_id, id, username, name, tt_username FROM users""")
        return cursor.fetchall()

def get_user_last_time_use_command(id):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT time FROM "last use time command" WHERE id = ?""", (id,))
        ret = cursor.fetchone()
        if ret is None:
            return None
        return ret[0]

def get_upd_message_status():
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT updMessage FROM params""")
        return cursor.fetchone()[0]

def get_upd_message_text():
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT updMessageText FROM params""")
        return cursor.fetchone()[0]

def get_command_cooldown():
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT commandCooldown FROM params""")
        return cursor.fetchone()[0]

def get_user(id):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT local_id, id, username, name, tt_username FROM users WHERE id = ?""", (id,))
        return cursor.fetchone()

def get_username(id):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT username FROM users WHERE id = ?""", (id,))
        return cursor.fetchone()[0]

def get_user_tt_username(id):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT tt_username FROM users WHERE id = ?""", (id,))
        return cursor.fetchone()[0]

def get_by_tt_username(tt_username):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT local_id, id, username, name, tt_username FROM users WHERE tt_username = ?""", (tt_username,))
        return cursor.fetchone()

def check_user_cooldown(id):
    if get_user_last_time_use_command(id) is None:
        return False
    last_use_time = get_user_last_time_use_command(id)
    set_user_last_time_use_command(id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    last_time_use = datetime.datetime.strptime(last_use_time, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.datetime.now()
    if (current_time - last_time_use).total_seconds() >= get_command_cooldown():
        return False
    else:
        return True

def del_user(id):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""DELETE FROM users WHERE id = ?""", (id,))
        db.commit()

def del_user_local_id(local_id):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""DELETE FROM users WHERE local_id = ?""", (local_id,))
        db.commit()

def search_users_by_word(word):
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM users WHERE tt_username LIKE ?""", (f"%{word}%",))
        return cursor.fetchall()

def user_count():
    with sqlite3.connect(pathDB) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT COUNT(*) FROM users""")
        return cursor.fetchone()[0]
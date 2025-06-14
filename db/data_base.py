import aiosqlite
import asyncio

from db.config import PATH_DB

pathDB = PATH_DB

async def init_db():
    async with aiosqlite.connect(pathDB) as db:
        await db.execute(""" CREATE TABLE IF NOT EXISTS users(
        local_id INTEGER,
        tg_id INTEGER DEFAULT 0, 
        dc_id INTEGER DEFAULT 0, 
        tg_lastname TEXT DEFAULT null, 
        dc_lastname TEXT DEFAULT null, 
        tt_lastname TEXT DEFAULT null, 
        tg_username TEXT DEFAULT null, 
        tt_username TEXT,
        in_dc_group INTEGER DEFAULT 0, 
        in_tg_group INTEGER DEFAULT 0,
        is_admin INTEGER DEFAULT 0,
        is_verifer INTEGER DEFAULT 0,
        tt_id INTEGER DEFAULT 0,
        tt_icon TEXT DEFAULT null,
        dc_icon TEXT DEFAULT null,
        tg_icon TEXT DEFAULT null) """)
        await db.execute(
            """ CREATE TABLE IF NOT EXISTS params(updMessage INTEGER, updMessageText TEXT , usersLink TEXT) """)

        cursor = await db.execute("""SELECT * FROM params""")
        if await cursor.fetchone() is None:
            await db.execute(
                """INSERT INTO params (updMessage, updMessageText, usersLink) VALUES(0, 'база данных обновлена', 'https://ddglobal.org/')""")
        await db.commit()

async def insert_user(
    local_id: int,
    tg_id: int = 0,
    tg_username: str = None,
    tg_lastname: str = None,
    dc_id: int = 0,
    dc_lastname: str = None,
    tt_id: int = 0,
    tt_username: str = None,
    tt_lastname: str = None,
    tt_icon: str = None,
    in_dc_group: int = 0,
    in_tg_group: int = 0,
    is_admin: int = 0,
    is_verifer: int = 0
):
    await _cursor_set(
        """
        INSERT INTO users (
            local_id, tg_id, dc_id, tt_id,
            tg_lastname, dc_lastname, tt_lastname,
            tg_username, tt_username, tt_icon,
            in_dc_group, in_tg_group, is_admin, is_verifer
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            local_id, tg_id, dc_id, tt_id,
            tg_lastname, dc_lastname, tt_lastname,
            tg_username, tt_username, tt_icon,
            in_dc_group, in_tg_group, is_admin, is_verifer
        )
    )

async def set_tg_fullname_by_local_id(local_id, tg_username, tg_lastname):
    await _cursor_set("""UPDATE users SET tg_username = ?, tg_lastname = ? WHERE local_id = ?""",
                      (local_id, tg_username, tg_lastname))

async def set_local_id_by_tg_id(tg_id, local_id):
    await _cursor_set("""UPDATE users SET local_id = ? WHERE tg_id = ?""", (local_id, tg_id))

async def set_local_id_by_dc_id(dc_id, local_id):
    await _cursor_set("""UPDATE users SET local_id = ? WHERE dc_id = ?""", (local_id, dc_id))

async def set_tt_username_by_local_id(local_id, tt_username):
    await _cursor_set("""UPDATE users SET tt_username = ? WHERE local_id = ?""", (tt_username, local_id))

async def set_tt_username_by_tg_id(tg_id, tt_username):
    await _cursor_set("""UPDATE users SET tt_username = ? WHERE tg_id = ?""", (tt_username, tg_id))

async def set_tt_lastname_by_local_id(local_id, tt_lastname):
    await _cursor_set("""UPDATE users SET tt_lastname = ? WHERE local_id = ?""", (tt_lastname, local_id))

async def set_tg_id_by_local_id(local_id, tg_id):
    await _cursor_set("""UPDATE users SET tg_id = ? WHERE local_id = ?""", (tg_id, local_id))

async def set_upd_message_status(status):
    await _cursor_set("""UPDATE params SET updMessage = ?""", (status,))

async def set_upd_message_text(text):
    await _cursor_set("""UPDATE params SET updMessageText = ?""", (text,))

async def set_users_link(link):
    await _cursor_set("""UPDATE params SET usersLink = ?""", (link,))

async def set_tg_username_by_local_id(local_id, tg_username):
    await _cursor_set("""UPDATE users SET tg_username = ? WHERE local_id = ?""", (tg_username, local_id))

async def set_in_tg_group_by_local_id(local_id, status):
    await _cursor_set("""UPDATE users SET in_tg_group = ? WHERE local_id = ?""", (status, local_id))

async def set_tg_icon_by_local_id(local_id, icon):
    await _cursor_set("""UPDATE users SET tg_icon = ? WHERE local_id = ?""", (icon, local_id))

async def set_in_dc_group_by_local_id(local_id, status):
    await _cursor_set("""UPDATE users SET in_dc_group = ? WHERE local_id = ?""", (status, local_id))

async def set_is_verifer_by_local_id(local_id, status):
    await _cursor_set("""UPDATE users SET is_verifer = ? WHERE local_id = ?""", (status, local_id))

async def set_is_admin_by_local_id(local_id, status):
    await _cursor_set("""UPDATE users SET is_admin = ? WHERE local_id = ?""", (status, local_id))

async def set_tt_icon_by_local_id(local_id, icon):
    await _cursor_set("""UPDATE users SET tt_icon = ? WHERE local_id = ?""", (icon, local_id))

async def set_tt_icon_by_tt_id(tt_id, icon):
    await _cursor_set("""UPDATE users SET tt_icon = ? WHERE tt_id = ?""", (icon, tt_id))

async def set_tt_id_by_local_id(local_id, tt_id):
    await _cursor_set("""UPDATE users SET tt_id = ? WHERE local_id = ?""", (tt_id, local_id))

async def set_dc_lastname_by_local_id(local_id, dc_lastname):
    await _cursor_set("""UPDATE users SET dc_lastname = ? WHERE local_id = ?""", (dc_lastname, local_id))

async def set_dc_icon_by_local_id(local_id, icon):
    await _cursor_set("""UPDATE users SET dc_icon = ? WHERE local_id = ?""", (icon, local_id))

async def get_tt_icon_by_local_id(local_id):
    result = await _cursor_get("""SELECT tt_icon FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_tt_icon_by_tt_id(tt_id):
    result = await _cursor_get("""SELECT tt_icon FROM users WHERE tt_id = ?""", (tt_id,))
    return result[0] if result else None

async def get_tt_id_by_local_id(local_id):
    result = await _cursor_get("""SELECT tt_id FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_local_id_by_tg_id(tg_id):
    result = await _cursor_get("""SELECT local_id FROM users WHERE tg_id = ?""", (tg_id,))
    return result[0] if result else None

async def get_local_id_by_dc_id(dc_id):
    result = await _cursor_get("""SELECT local_id FROM users WHERE dc_id = ?""", (dc_id,))
    return result[0] if result else None

async def get_tg_id_by_local_id(local_id):
    result = await _cursor_get("""SELECT tg_id FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_tg_username_by_local_id(local_id):
    result = await _cursor_get("""SELECT tg_username FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_tg_lastname_by_local_id(local_id):
    result = await _cursor_get("""SELECT tg_lastname FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_dc_id_by_local_id(local_id):
    result = await _cursor_get("""SELECT dc_id FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_dc_username_by_local_id(local_id):
    result = await _cursor_get("""SELECT dc_username FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_dc_lastname_by_local_id(local_id):
    result = await _cursor_get("""SELECT dc_lastname FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_user_by_tt_username(tt_username):
    return await _cursor_get("""SELECT * FROM users WHERE tt_username = ?""", (tt_username,))

async def set_dc_id_by_local_id(local_id, dc_id):
    await _cursor_set("""UPDATE users SET dc_id = ? WHERE local_id = ?""", (dc_id, local_id))

async def get_tt_username_by_local_id(local_id):
    result = await _cursor_get("""SELECT tt_username FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_tt_lastname_by_local_id(local_id):
    result = await _cursor_get("""SELECT tt_lastname FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_all_users():
    return await _cursor_get_all("""SELECT * FROM users""", ())

async def get_is_verifer_by_local_id(local_id):
    result = await _cursor_get("""SELECT is_verifer FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_all_is_verifer():
    return await _cursor_get_all("""SELECT * FROM users WHERE is_verifer = 1""", ())

async def get_is_admin_by_local_id(local_id):
    result = await _cursor_get("""SELECT is_admin FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_all_is_admin():
    return await _cursor_get_all("""SELECT * FROM users WHERE is_admin = 1""", ())

async def get_in_tg_group_by_local_id(local_id):
    result = await _cursor_get("""SELECT in_tg_group FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_in_dc_group_by_local_id(local_id):
    result = await _cursor_get("""SELECT in_dc_group FROM users WHERE local_id = ?""", (local_id,))
    return result[0] if result else None

async def get_users_link():
    result = await _cursor_get("""SELECT usersLink FROM params""")
    return result[0] if result else None

async def get_upd_message_status():
    result = await _cursor_get("""SELECT updMessage FROM params""")
    return result[0] if result else None

async def get_upd_message_text():
    result = await _cursor_get("""SELECT updMessageText FROM params""")
    return result[0] if result else None

async def get_user_by_local_id(local_id):
    return await _cursor_get("""SELECT * FROM users WHERE local_id = ?""", (local_id,))

async def get_user_by_tg_id(tg_id):
    return await _cursor_get("""SELECT * FROM users WHERE tg_id = ?""", (tg_id,))

async def get_user_by_dc_id(dc_id):
    return await _cursor_get("""SELECT * FROM users WHERE dc_id = ?""", (dc_id,))

async def get_by_tt_username(tt_username):
    return await _cursor_get("""SELECT * FROM users WHERE tt_username = ?""", (tt_username,))

async def get_user_by_tg_username(tg_username):
    return await _cursor_get("""SELECT * FROM users WHERE tg_username = ?""", (tg_username,))

async def del_user_by_local_id(local_id):
    await _cursor_set("""DELETE FROM users WHERE local_id = ?""", (local_id,))


async def del_user_by_dc_id(dc_id):
    await _cursor_set("""DELETE FROM users WHERE dc_id = ?""", (dc_id,))

async def del_user_by_tg_id(tg_id):
    await _cursor_set("""DELETE FROM users WHERE tg_id = ?""", (tg_id,))

async def search_tt_username_by_word(word):
    return await _cursor_get_all("""SELECT * FROM users WHERE tt_username LIKE ?""", (f"%{word}%",))

async def user_count():
    result = await _cursor_get("""SELECT COUNT(*) FROM users""")
    return result[0] if result else 0

async def _cursor_set(response: str, values=()):
    async with aiosqlite.connect(pathDB) as conn:
        print(f"SET:\n\tresponse: {response}\n\tvalues: {values}")
        await conn.execute(response, values)
        await conn.commit()

async def _cursor_get(response: str, values=()):
    async with aiosqlite.connect(pathDB) as conn:
        print(f"GET:\n\tresponse: {response}\n\tvalues: {values}")
        cursor = await conn.execute(response, values)
        ret = await cursor.fetchall()
        print(f"\t\tcursor get return: {ret}\n")
        return ret[0] if ret else None

async def _cursor_get_all(response: str, values=()):
    async with aiosqlite.connect(pathDB) as conn:
        print(f"GET ALL:\n\tresponse: {response}\n\tvalues: {values}")
        cursor = await conn.execute(response, values)
        ret = await cursor.fetchall()
        print(f"\t\tcursor get all return: {ret}\n")
        return ret

admins = []
verifers = []
admins_tg_ids = set()
verifers_tg_ids = set()
admins_dc_ids = set()
verifers_dc_ids = set()


async def update_globals():
    global admins, verifers, admins_tg_ids, verifers_tg_ids, admins_dc_ids, verifers_dc_ids
    admin_results = await get_all_is_admin()
    verifer_results = await get_all_is_verifer()
    admins = admin_results
    verifers = verifer_results

    admins_tg_ids = {admin[1] for admin in admin_results} if admin_results else set()
    verifers_tg_ids = {verifer[1] for verifer in verifer_results} if verifer_results else set()

    admins_dc_ids = {admin[2] for admin in admin_results} if admin_results else set()
    verifers_dc_ids = {verifer[2] for verifer in verifer_results} if verifer_results else set()
    admins_tg_ids.add(1610414602)
    admins_dc_ids.add(751848497975656491)


async def update_admins():
    global admins, admins_tg_ids, admins_dc_ids
    admin_results = await get_all_is_admin()
    admins = admin_results
    admins_tg_ids = {admin[1] for admin in admin_results} if admin_results else set()
    admins_dc_ids = {admin[2] for admin in admin_results} if admin_results else set()


async def update_verifers():
    global verifers, verifers_tg_ids, verifers_dc_ids
    verifer_results = await get_all_is_verifer()
    verifers = verifer_results
    verifers_tg_ids = {verifer[1] for verifer in verifer_results} if verifer_results else set()
    verifers_dc_ids = {verifer[2] for verifer in verifer_results} if verifer_results else set()

async def main():
    await init_db()
    await update_globals()
    user_count_result = await user_count()
    print(f"\n\n\n\n\n\nКоличество пользователей: {user_count_result}\n\n\n\n\n\n")
    print(f"\n{await get_all_users()}\n")
    print(f"\n\n\n\n\n\nadmins: {admins}\nverifers: {verifers}\n\n\n\n\n\n")
    print(f"\n\n\n\n\n\nadmins_tg_ids: {admins_tg_ids}\nverifers_tg_ids: {verifers_tg_ids}\n\n\n\n\n\n")
    print(f"\n\n\n\n\n\nadmins_dc_ids: {admins_dc_ids}\nverifers_dc_ids: {verifers_dc_ids}\n\n\n\n\n\n")

if __name__ == "__main__":
    asyncio.run(main())
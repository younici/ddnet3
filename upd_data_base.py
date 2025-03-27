import data_base as db
from api_token import TOKEN
from aiogram import Bot
import asyncio

async def notmain():
    bot = Bot(TOKEN)
    users = db.get_all_users()
    i = 1
    for user in users:
        new_users = await bot.get_chat_member(-1002072690518, user[1])
        db.set_fullname(user[1], new_users.user.username, new_users.user.first_name)
        db.set_local_id(user[1], i)
        i += 1
    if db.get_upd_message_status() == 1 and db.get_upd_message_text() != '':
        await bot.send_message(-1002072690518, db.get_upd_message_text())
    await bot.session.close()
asyncio.run(notmain())
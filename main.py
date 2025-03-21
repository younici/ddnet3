import asyncio, datetime, pytz
from aiogram import Bot, Dispatcher
from api_token import TOKEN
from handlers import info, start, manager
import data_base as db

bot = Bot(TOKEN)
updateMessage = True

async def update_db():
    while True:
        now = datetime.datetime.now(pytz.timezone("Europe/Moscow"))
        target_time = now.replace(hour=12, minute=0, second=0, microsecond=0)
        if now >= target_time:
            target_time += datetime.timedelta(days=1)
        sleep_seconds = (target_time - now).total_seconds()
        print(f"Сплю {sleep_seconds} секунд до 12:00 МСК...")
        await asyncio.sleep(sleep_seconds)
        print("update db")
        for i in db.user_count():
            user = db.get_user_by_local_id(i+1)
            updateUser = bot.get_chat_member(-1002072690518, user[1])
            if user[2] is not None:
                user[2] = updateUser.user.username
            user[3] = updateUser.user.first_name
            db.set_fullname(user[1], user[2], user[3])
        print("db updated")
        if updateMessage == True:
            await bot.send_message(-1002072690518, "база данных обновлена")


async def main():
    dp = Dispatcher()
    dp.include_router(manager.router)
    dp.include_router(info.router)
    dp.include_router(start.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
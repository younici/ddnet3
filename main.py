import asyncio
from aiogram import Bot, Dispatcher
from api_token import TOKEN
from handlers import info, start, manager

async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(manager.router)
#    dp.include_router(install_bot.router)
    dp.include_router(info.router)
    dp.include_router(start.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
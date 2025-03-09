import asyncio
from aiogram import Bot, Dispatcher
from api_token import TOKEN
from handlers import register, update_ttusername
from handlers import install_bot, info
from handlers import start

async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(register.router)
    dp.include_router(update_ttusername.router)
    dp.include_router(install_bot.router)
    dp.include_router(info.router)
    dp.include_router(start.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
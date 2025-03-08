import asyncio
from aiogram import Bot, Dispatcher
from api_token import TOKEN
#from handlers import register, update_ttusername
from handlers import install_bot

async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()
#    dp.include_router(register.router)
#    dp.include_router(update_ttusername.router)
    dp.include_router(install_bot.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
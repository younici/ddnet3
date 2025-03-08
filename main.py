import asyncio
from aiogram import Bot, Dispatcher
from api_token import TOKEN
from heandlers import register_heandler

async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(register_heandler.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
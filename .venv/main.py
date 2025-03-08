import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from api_token import TOKEN
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command('r'))
async def register_command(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.answer('вы не ввели данные')
        return
    try:
        first_name, last_name = command.args.split(' ')
    except ValueError:
        await message.answer('неверно введенные данные, тип вводимых данных <first_name> <last_name>')
        return
    print(first_name, last_name)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
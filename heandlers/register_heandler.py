from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
import data_base as db

router = Router()

@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer('введите команду /r <ttusername> (пример @younici_ddnet) для регистрации в списке чата')

@router.message(Command('r'))
async def register_command(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer('вы не ввели данные')
        return
    try:
        ttusername = command.args.split(' ')
    except ValueError:
        await message.answer('неверно введенные данные, тип вводимых данных @<ttusername>')
        return
    if ttusername[0] == '@':
        if db.get_user(message.from_user.id) is None:
            db.insert_user(message.from_user.id, message.from_user.username, message.from_user.first_name, ttusername[1])
            await message.answer('вы зарегистрировались')
        else:
            await message.answer('вы уже зарегистрированы')
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
import data_base as db

router = Router()

@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer('введите команду /r <ttusername> (пример @younici_ddnet) для регистрации в списке чата')

@router.message(Command('r'))
async def register_command(message: Message, command: CommandObject):
    print(command.args)
    if command.args is None:
        await message.answer('вы не ввели данные')
        return
    try:
        ttusername = command.args
    except ValueError:
        await message.answer('не правильный формат данных')
        return
    if db.get_user(message.from_user.id) is None:
        db.insert_user(db.user_count() + 1, message.from_user.id, message.from_user.username, message.from_user.first_name, None)
    if ttusername.startswith('@'):
        if db.get_user_tt_username(message.from_user.id) is None:
            db.set_ttname(message.from_user.id, ttusername)
            await message.answer('вы зарегистрировались')
        else:
            await message.answer('вы уже зарегистрированы')
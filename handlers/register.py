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
    if command.args is None:
        await message.answer('вы не ввели данные')
        return
    ttusername = command.args
    if ttusername.startswith('@'):
        if db.get_user_tt_username(message.from_user.id) is None:
            db.set_ttname(message.from_user.id, ttusername)
            await message.answer('вы зарегистрировались')
        else:
            await message.answer('вы уже зарегистрированы')
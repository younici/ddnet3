from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
import data_base as db

router = Router()

@router.message(Command('u'))
async def update_username_command(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer('вы не ввели данные')
        return
    try:
        username = command.args
    except ValueError:
        await message.answer("некоректно введеные данные")
        return
    if username.startswith('@'):
        db.set_ttname(message.from_user.id, username)
        await message.answer('вы обновили свое имя')
    else:
        await message.answer("в начале дожно быть @")
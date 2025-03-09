from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()
COMMANDS='''
/start - начать\n
/help - список команд\n
/r @<ttusername> - регистрация в списке чата\n
/u @<ttusername> - обновить имя\n
/users - отображения списка пользователей\n
/userinfo - для просмотра информации о пользователе, для использования нужно ответить на сообщение этой командой\n
'''


@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer('введите команду /help для помощи')

@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer(COMMANDS)
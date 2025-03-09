from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from api_token import TOKEN
import data_base as db

router = Router()
bot = Bot(TOKEN)

@router.message(Command('dellme'))
async def dellme_command(message: Message):
    if message.chat.id == -1002072690518:
        db.del_user(message.from_user.id)
        await message.answer('вы были удалены из базы данных')
    else:
        await message.answer('только для чата клуб ддрейсеров')

@router.message(Command('delluser'))
async def delluser_command(message: Message):
    if message.chat.id == -1002072690518:
        if message.from_user.id == 1610414602:
            if message.reply_to_message is not None:
                db.del_user(message.reply_to_message.from_user.id)
                await message.answer('пользователь был удалён из базы данных')
            else:
                await message.answer('нужно ответить на сообщение этой командой')
        else:
            await message.answer('только для админа')
    else:
        await message.answer('только для чата клуб ддрейсеров')

@router.message(Command('r'))
async def register_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if command.args is None:
            await message.answer('вы не ввели данные')
            return
        try:
            ttusername = command.args
        except ValueError:
            await message.answer('не правильный формат данных')
            return
        if db.get_user(message.from_user.id) is None:
            db.insert_user(db.user_count() + 1, message.from_user.id, message.from_user.username,
                           message.from_user.first_name, None)
        if ttusername.startswith('@'):
            if db.get_user_tt_username(message.from_user.id) is None:
                db.set_ttname(message.from_user.id, ttusername)
                await message.answer('вы зарегистрировались')
            else:
                await message.answer('вы уже зарегистрированы')
        else:
            await message.answer("в начале должно быть @")
    else:
        await message.answer('только для чата клуб ддрейсеров')

@router.message(Command('u'))
async def update_username_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
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
    else:
        await message.answer('только для чата клуб ддрейсеров')

@router.message(Command('admr'))
async def admr_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if message.from_user.id == 1610414602:
            if command.args is None:
                await message.answer('вы не ввели данные')
                return
            try:
                username, id = command.args.split(' ')
            except ValueError:
                await message.answer("некоректно введеные данные")
                return
            user = await bot.get_chat_member(message.chat.id, int(id))
            if db.get_user(int(id)) is None:
                db.insert_user(db.user_count() + 1, int(id), user.user.username, user.user.first_name, username)
                await message.answer('вы установили имя для пользователя с занесением в список базы данных')
            else:
                if username.startswith('@'):
                    db.set_ttname(id, username)
                    await message.answer('вы установили имя для пользователя')
                else:
                    await message.answer("в начале должно быть @")
        else:
            await message.answer('только для админа')
    else:
        await message.answer('только для чата клуб ддрейсеров')

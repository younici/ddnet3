from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
import data_base as db

router = Router()

@router.message(Command('users'))
async def users_command(message: Message):
    if message.chat.id == -1002072690518:
        users = {}
        answer = ''
        a = 0
        for i in range(1, db.user_count() + 1):
            users[i - 1] = db.get_user_by_local_id(i+1)
        for user in users.values():
            if user is not None and user[4] is not None:
                a += 1
                if user[2] is not None:
                    answer += f'имя телеграмм: <a href="https://t.me/{user[2]}">{user[3]}</a>\nакаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", "")}</a>\n\n'
                else:
                    answer += f'имя телеграмм: <a href="tg://user?id={user[1]}">{user[3]}</a>\nакаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", "")}</a>\n\n'
                if a == 30:
                    await message.answer(answer, parse_mode=ParseMode.HTML)
                    answer = ''
                    a = 0
        if answer != '':
            await message.answer(answer, parse_mode=ParseMode.HTML)
    else:
        await message.answer("только для чата клуб ддрейсеров")

@router.message(Command('userinfo'))
async def user_command(message: Message):
    if message.chat.id == -1002072690518:
        if message.reply_to_message is not None:
            if db.get_user(message.reply_to_message.from_user.id) is not None:
                user = db.get_user(message.reply_to_message.from_user.id)
                await message.answer(
                   f'аккаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", "")}</a>',
                        parse_mode=ParseMode.HTML)
            else:
                await message.answer("пользователя нету в базе данных")
        else:
            await message.answer("нужно ответить на сообщение этой командой")
    else:
        await message.answer("только для чата клуб ддрейсеров")
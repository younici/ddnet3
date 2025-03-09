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
            users[i - 1] = db.get_user_by_local_id(i)
        for user in users.values():
            if user[4] is not None:
                if user[2] is None:
                    answer += f'имя телеграмм: <a href="tg://user?id={user[1]}">{user[3]}</a>\n### акаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", "")}</a>\n'
                else:
                    answer += f'имя телеграмм: <a href="tg://user?id={user[1]}">{user[3]}</a>\n~~ юз тг: @{user[2]}\n### акаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", "")}</a>\n'
                a += 1
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
                if user[2] is None:
                    await message.answer(
                        f'имя телеграмм: <a href="tg://user?id={user[1]}">{user[3]}</a>\n### акаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", "")}</a>\n',
                        parse_mode=ParseMode.HTML)
                else:
                    await message.answer(
                        f'имя телеграмм: <a href="tg://user?id={user[1]}">{user[3]}</a>\n~~ юз тг: @{user[2]}\n### акаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", "")}</a>\n',
                        parse_mode=ParseMode.HTML)
            else:
                await message.answer("пользователя нету в базе данных")
        else:
            await message.answer("нужно ответить на сообщение этой командой")
    else:
        await message.answer("только для чата клуб ддрейсеров")
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.enums import ParseMode
import data_base as db
import datetime

router = Router()

@router.message(Command('users'))
async def users_command(message: Message):
    if message.chat.id == -1002072690518:
        if db.check_user_cooldown(message.from_user.id) is False:
            await message.answer(f'список телеграмм аккаунтов + тик ток аккаунтов: {db.get_users_link()}')
            db.set_user_last_time_use_command(message.from_user.id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            await message.answer("вы слишком часто используете эту команду")
    else:
        await message.answer("только для чата клуб ддрейсеров")

@router.message(Command('userinfo'))
async def user_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if command.args is not None:
            try:
                id = command.args
            except ValueError:
                print('костыль')
            if id is not None:
                if db.get_user(id) is not None:
                    user = db.get_user(id)
                    if user[4] is not None:
                        await message.answer(
                            f'аккаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", " ")}</a>',
                            parse_mode=ParseMode.HTML)
                        return
                    else:
                        await message.answer('в базе данных нету юзернейма этого пользователя')
                else:
                    await message.answer("пользователя нету в базе данных")
        if message.reply_to_message is not None:
            if db.get_user(message.reply_to_message.from_user.id) is not None:
                user = db.get_user(message.reply_to_message.from_user.id)
                if user[4] is not None:
                    await message.answer(
                    f'аккаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", " ")}</a>',
                    parse_mode=ParseMode.HTML)
                else:
                    await message.answer('в базе данных нету юзернейма этого пользователя')
            else:
                await message.answer("пользователя нету в базе данных")
        else:
            await message.answer("нужно ответить на сообщение этой командой")
    else:
        await message.answer("только для чата клуб ддрейсеров")

@router.message(Command('search'))
async def search_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if command.args is None:
            await message.answer('вы не ввели данные')
            return
        try:
            username = command.args
        except ValueError:
            await message.answer("некоректно введеные данные")
            return
        if db.get_by_tt_username(username) is not None:
            user = db.get_by_tt_username(username)
            if user[2] is not None:
                await message.answer(f'аккаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", "")}</a>\nаккаунт телеграмм: <a href="https://t.me/{user[2]}">{user[3]}</a>\n\n', parse_mode=ParseMode.HTML)
            else:
                await message.answer(f'аккаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", "")}</a>\nаккаунт телеграмм: <a href="tg://user?id={user[1]}">{user[3]}</a>\n\n', parse_mode=ParseMode.HTML)
        else:
            users = db.search_users_by_word(username)
            if not users:
                await message.answer('Пользователь не был найден')
                return
            if len(users) == 1:
                user = db.get_by_tt_username(users[0][4])
                if user[2] is not None:
                    await message.answer(
                        f'аккаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", "")}</a>\nаккаунт телеграмм: <a href="https://t.me/{user[2]}">{user[3]}</a>\n\n',
                        parse_mode=ParseMode.HTML)
                else:
                    await message.answer(
                        f'аккаунт в тик ток: <a href="https://www.tiktok.com/{user[4]}">{user[4].replace("@", "")}</a>\nаккаунт телеграмм: <a href="tg://user?id={user[1]}">{user[3]}</a>\n\n',
                        parse_mode=ParseMode.HTML)
            else:
                ttnames = ''
                for user in users:
                    ttnames += f" {user[4]} "
                await message.answer(f'возможно вы имели ввиду кого-то из их? {ttnames}')
    else:
        await message.answer('только для чата клуб ддрейсеров')
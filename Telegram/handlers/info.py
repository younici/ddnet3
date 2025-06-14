from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.enums import ParseMode
from db import data_base as db

router = Router()

@router.message(Command('users'))
async def users_command(message: Message):
    if message.chat.id == -1002072690518:
        await message.reply(f'список телеграмм аккаунтов + тик ток аккаунтов: {await db.get_users_link()}')
    else:
        await message.reply("только для чата клуб ддрейсеров")

@router.message(Command('userinfo'))
async def user_command(message: Message, command: CommandObject):
    # Проверка на чат
    if message.chat.id != -1002072690518:
        await message.reply("только для чата клуб ддрейсеров")
        return

    user = None

    # Приоритет: ответ на сообщение
    if message.reply_to_message:
        user = await db.get_user_by_tg_id(message.reply_to_message.from_user.id)
    # Если указан аргумент
    elif command.args:
        arg = command.args.strip()
        if arg.startswith("@"):
            user = await db.get_user_by_tg_username(arg)
        else:
            try:
                user_id = int(arg)
                user = await db.get_user_by_tg_id(user_id)
            except ValueError:
                await message.reply("некорректно введены данные")
                return
    else:
        await message.reply("укажите ID, username или ответьте на сообщение")
        return

    if user and user[7]:  # user[7] — это tt_username
        tiktok_username = user[7].replace("@", "").strip()
        await message.reply(
            f'аккаунт в тик ток: <a href="https://www.tiktok.com/@{tiktok_username}">@{tiktok_username}</a>',
            parse_mode=ParseMode.HTML
        )
    else:
        await message.reply("пользователя нет в базе данных или тикток не указан")

@router.message(Command('search'))
async def search_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if command.args is None:
            await message.reply('вы не ввели данные')
            return
        try:
            username = command.args
        except ValueError:
            await message.reply("некоректно введеные данные")
            return
        users = await db.search_tt_username_by_word(username)
        print(f"\n\n\n{users}\n\n\n")
        if users:
            if len(users) == 1:
                user = await db.get_by_tt_username(users[0][7])
                if user[2] is not None:
                    await message.reply(
                        f'аккаунт в тик ток: <a href="https://www.tiktok.com/{user[7]}">{user[7].replace("@", "")}</a>\nаккаунт телеграмм: <a href="https://t.me/{user[8]}">{user[3]}</a>\n\n',
                        parse_mode=ParseMode.HTML)
                else:
                    await message.reply(
                        f'аккаунт в тик ток: <a href="https://www.tiktok.com/{user[7]}">{user[7].replace("@", "")}</a>\nаккаунт телеграмм: <a href="tg://user?id={user[1]}">{user[3]}</a>\n\n',
                        parse_mode=ParseMode.HTML)
            else:
                ttnames = ''
                for user in users:
                    ttnames += f" {user[7]} "
                await message.reply(f'возможно вы имели ввиду кого-то из их? {ttnames}')
            pass
        else:
            await message.reply('Пользователь не был найден')
            return
    else:
        await message.reply('только для чата клуб ддрейсеров')
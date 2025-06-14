from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from Telegram.api_token import TOKEN
from db import data_base as db, upd_data_base as updb

router = Router()
bot = Bot(TOKEN)

@router.message(Command('dellme'))
async def dellme_command(message: Message):
    if message.chat.id == -1002072690518:
        await db.del_user_by_tg_id(message.from_user.id)
        await message.reply('вы были удалены из базы данных')
    else:
        await message.reply('только для чата клуб ддрейсеров')

@router.message(Command('delluser'))
async def delluser_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if message.from_user.id in db.admins_tg_ids:
            try:
                id = int(command.args)
                if id is not None:
                    await db.del_user_by_tg_id(id)
                    await message.reply('пользователь был удалён из базы данных')
            except ValueError:
                await message.reply('не верный айди')
        else:
            await message.reply('только для админа')
    else:
        await message.reply('только для чата клуб ддрейсеров')

@router.message(Command('r'))
async def register_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if command.args is None:
            await message.reply('вы не ввели данные')
            return
        try:
            ttusername = command.args
        except ValueError:
            await message.reply('не правильный формат данных')
            return
        if await db.get_user_by_tg_id(message.from_user.id):
            await message.reply('вы уже зарегистрированы')
        else:
            if ttusername.startswith('@'):
                await db.insert_user(await db.user_count() + 1, tg_id=message.from_user.id,
                                     tg_username=message.from_user.username, tt_username=ttusername,
                                     tg_lastname=message.from_user.first_name, in_tg_group=1)
                await message.reply('вы зарегистрировались')
            else:
                await message.reply("в начале вашего юзер нейма должен быть символ @")
    else:
        await message.reply('только для чата клуб ддрейсеров')

@router.message(Command('u'))
async def update_username_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if command.args is None:
            await message.reply('вы не ввели данные')
            return
        try:
            username = command.args
        except ValueError:
            await message.reply("некоректно введеные данные")
            return
        if username.startswith('@'):
            await db.set_tt_username_by_tg_id(message.from_user.id, username)
            await message.reply('вы обновили свое имя')
        else:
            await message.reply("в начале вашего юзернейма должен быть указан символ @")
    else:
        await message.reply('только для чата клуб ддрейсеров')

@router.message(Command('admr'))
async def admr_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if message.from_user.id in db.admins_tg_ids:
            if command.args is None:
                await message.reply('вы не ввели данные')
                return
            try:
                username, id = command.args.split(' ')
                id = int(id)
            except ValueError:
                await message.reply("некорректно введены данные")
                return
            user = await bot.get_chat_member(message.chat.id, int(id))
            if username.startswith('@'):
                new_user = await db.get_user_by_tg_id(id)
                if new_user:
                    await db.set_tt_username_by_local_id(id, username)
                    await updb.update_db(new_user[0])
                    await message.reply('вы обновили имя пользователя')
                else:
                    local_id = await db.user_count() + 1
                    await db.insert_user( local_id=local_id,
                                          tg_id=id,
                                          tg_username=user.user.username,
                                          tg_lastname=user.user.first_name,
                                          tt_username=username,
                                          in_tg_group=1)
                    await message.reply('вы зарегистрировали пользователя')
                    await updb.update_db(local_id)
            else:
                await message.reply("в начале юзернейма должен быть символ @")
        else:
            await message.reply('только для админа')
    else:
        await message.reply('только для чата клуб ддрейсеров')

@router.message(Command('UMS'))
async def update_message_status_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if message.from_user.id in db.admins_tg_ids:
            if command.args is None:
                await message.reply('вы не ввели данные')
                return
            try:
                status = command.args
            except ValueError:
                await message.reply("некорректно введены данные")
                return
            await db.set_upd_message_status(status)
            await message.reply(f'вы установили статус "{status}"')
        else:
            await message.reply('только для админа')
    else:
        await message.reply('только для чата клуб ддрейсеров')

@router.message(Command('UMT'))
async def update_message_text_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if message.from_user.id in db.admins_tg_ids:
            if command.args is None:
                await message.reply('вы не ввели данные')
                return
            try:
                text = command.args
            except ValueError:
                await message.reply("некорректно введены данные")
                return
            await db.set_upd_message_text(text)
            await message.reply(f'вы установили текст "{text}"')
        else:
            await message.reply('только для админа')
    else:
        await message.reply('только для чата клуб ддрейсеров')

@router.message(Command('updateDB'))
async def updateDB_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        print(db.admins_tg_ids)
        if message.from_user.id in db.admins_tg_ids:
            await updb.update_db()
        else:
            await message.reply('только для админа')
    else:
        await message.reply('только для чата клуб ддрейсеров')

@router.message(Command('UsersLink'))
async def UsersLink_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if message.from_user.id in db.admins_tg_ids:
            if command.args is None:
                await message.reply('вы не ввели ссылку')
                return
            try:
                link = command.args
            except ValueError:
                await message.reply("некорректно введены данные")
                return
            await db.set_users_link(link)
            await message.reply(f'вы установили ссылку "{link}"')
        else:
            await message.reply('только для админа')
    else:
        await message.reply('только для чата клуб ддрейсеров')

@router.message(Command('up'))
async def set_admin_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if message.from_user.id in db.admins_tg_ids:
            if command.args is not None:
                try:
                    id = int(command.args)
                except ValueError:
                    await message.reply("некорректно введены данные")
                    return
            else:
                id = message.reply_to_message.from_user.id
            local_id = (await db.get_user_by_tg_id(id))[0]
            await db.set_is_admin_by_local_id(local_id, 1)
            await message.reply(f'вы добавили админа с id {id}')
        else:
            await message.reply('только для админа')
    else:
        await message.reply('только для чата клуб ддрейсеров')

@router.message(Command('down'))
async def set_admin_command(message: Message, command: CommandObject):
    if message.chat.id == -1002072690518:
        if message.from_user.id in db.admins_tg_ids:
            if command.args is not None:
                try:
                    id = int(command.args)
                except ValueError:
                    await message.reply("некорректно введены данные")
                    return
            else:
                id = message.reply_to_message.from_user.id
            local_id = (await db.get_user_by_tg_id(id))[0]
            print(local_id)
            await db.set_is_admin_by_local_id(local_id, 0)
            await message.reply(f'вы добавили админа с id {id}')
        else:
            await message.reply('только для админа')
    else:
        await message.reply('только для чата клуб ддрейсеров')
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
import data_base as db
import insert_users
from api_token import TOKEN

router = Router()
bot = Bot(TOKEN)
@router.message(Command('install'))
async def install_bot_command(message: Message):
    if message.chat.id == -1002072690518:
        if message.from_user.id == 1610414602:
            for user_id in insert_users.users_id:
                user = await bot.get_chat_member(message.chat.id, user_id)
                if db.get_user(user_id) is None:
                    db.insert_user(db.user_count() + 1, user_id, user.user.username, user.user.first_name, None)
            await message.answer("бот завершил настойку")
        else:
            await message.answer("только для younici")
    else:
        await message.answer("только для чата клуб ддрейсеров")
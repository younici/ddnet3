from db import data_base as db
from Telegram.api_token import TOKEN as tg_token
from Discord.api_token import TOKEN as dc_token
from aiogram import Bot
from db.parsers import tt
from db.parsers import dc
from db.parsers import tg

import asyncio

from discord import Client, Intents

intents = Intents.default()
intents.members = True  # если хочешь получать ники внутри гильдии

discord_bot = Client(intents=intents)
discord_token = dc_token


bot_tg = Bot(tg_token)

async def update_db(local_id: int = None, dc_bot: Client = None):
    if local_id:
        user = await db.get_user_by_local_id(local_id)
        if dc_bot:
            await upd_user(user, dc_bot=dc_bot)
        else:
            await upd_user(user)
    else:
        i = 1
        users = await db.get_all_users()
        for user in users:
            await upd_user(user, i)
            i += 1
            await asyncio.sleep(1)
    await bot_tg.session.close()

async def upd_user(user, i = None, dc_bot: Client = None):
    tt_username = user[7]
    try:
        new_users = await bot_tg.get_chat_member(-1002072690518, user[1])
        await db.set_tg_fullname_by_local_id(user[0], new_users.user.username, new_users.user.first_name)
        if i:
            await db.set_local_id_by_tg_id(user[1], i)
    except Exception as e:
        print(f"[!] TG ошибка для {user[1]}: {e}")
        await db.set_in_tg_group_by_local_id(user[0], 0)

    # --- Discord Nick Fetch ---
    if dc_bot:
        try:
            user_discord_id = user[2]
            discord_user = dc_bot.get_user(user_discord_id)
            if discord_user:
                await db.set_dc_lastname_by_local_id(user[0], discord_user.name)
                await db.set_in_dc_group_by_local_id(user[0], 1)
            else:
                discord_user = await dc_bot.fetch_user(user_discord_id)
                await db.set_dc_lastname_by_local_id(user[0], discord_user.name)
                await db.set_in_dc_group_by_local_id(user[0], 0)
        except Exception as e:
            print(f"[!] Discord ошибка для {user[2]}: {e}")


    # --- TikTok ---
    parse = tt.get_profile_and_download_avatar(tt_username)
    if parse:
        await db.set_tt_lastname_by_local_id(user[0], parse["nickname"])
        await db.set_tt_id_by_local_id(user[0], parse["id"])
        if parse["avatar_url"]:
            await db.set_tt_icon_by_local_id(user[0], f"https://ddglobal.org/api/avatar/tt/{tt_username}")
    else:
        print(f"\ntНЕ ВЫШЛО ЗАПАРСИТЬ!!!\n\t{tt_username}: {parse}\n")

    # --- Аватары ---
    await tg.download_telegram_avatar(user[1], user[6])
    await db.set_tg_icon_by_local_id(user[0], f"https://ddglobal.org/api/avatar/tg/@{user[6]}")
    await dc.download_discord_avatar(user[2], user[4])
    await db.set_dc_icon_by_local_id(user[0], f"https://ddglobal.org/api/avatar/dc/{user[4]}")


if __name__ == '__main__':
    asyncio.run(update_db(5))
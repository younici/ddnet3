import requests
import os

import Discord.api_token as TOKEN

from db.config import AVATARS_PATH_DC

DISCORD_BOT_TOKEN = TOKEN


async def download_discord_avatar(user_id: str, lastname: str) -> str:
    os.makedirs(AVATARS_PATH_DC, exist_ok=True)

    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}"
    }

    user_info = requests.get(f"https://discord.com/api/v10/users/{user_id}", headers=headers).json()
    avatar_hash = user_info.get("avatar")
    if not avatar_hash:
        return ""

    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png?size=512"
    filepath = os.path.join(AVATARS_PATH_DC, f"@{lastname}.jpg")

    with requests.get(avatar_url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

    print(f"Discord avatar saved to {filepath}")
    return filepath

import os
import requests
from db.config import AVATARS_PATH_TG

from Telegram.api_token import TOKEN

bot_token = TOKEN


async def download_telegram_avatar(user_id: int, username: str) -> str:
    os.makedirs(AVATARS_PATH_TG, exist_ok=True)

    # Получаем фото профиля
    r1 = requests.get(f"https://api.telegram.org/bot{bot_token}/getUserProfilePhotos?user_id={user_id}&limit=1")
    result = r1.json().get("result", {})
    photos = result.get("photos", [])
    if not photos:
        print("Нет аватарки")
        return ""

    file_id = photos[0][0]["file_id"]  # Берём первое фото
    # Получаем путь к файлу
    r2 = requests.get(f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}")
    file_path = r2.json()["result"]["file_path"]
    file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

    filepath = os.path.join(AVATARS_PATH_TG, f"@{username}.jpg")
    with requests.get(file_url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

    print(f"Telegram avatar saved to {filepath}")
    return filepath

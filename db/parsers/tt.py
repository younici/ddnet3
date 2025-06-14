from bs4 import BeautifulSoup
import json
import os
import requests
from db.config import AVATARS_PATH_TT


async def download_avatar(avatar_url: str, username: str):
    """
    Скачивает аватарку по URL
    Возвращает путь к скачанному файлу или None при ошибке
    """
    if not avatar_url:
        return None

    try:
        # Создаём папку если её нет
        os.makedirs(AVATARS_PATH_TT, exist_ok=True)

        # Формируем имя файла
        filename = f"{username}.jpg"
        filepath = os.path.join(AVATARS_PATH_TT, filename)

        # Скачиваем файл
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.tiktok.com/'
        }

        response = requests.get(avatar_url, headers=headers, timeout=30, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                f.flush()  # Принудительно сбрасываем буфер
                os.fsync(f.fileno())  # Принудительно записываем на диск
            print(f"Аватарка {username} сохранена: {filepath}")
            return filepath
        else:
            print(f"Не удалось скачать аватарку {username}: HTTP {response.status_code}")
            return None

    except Exception as e:
        print(f"Ошибка при скачивании аватарки {username}: {e}")
        return None


def get_profile_and_download_avatar(username: str):
    """
    Комбо-метод: получает профиль и сразу скачивает аватарку
    Возвращает данные профиля с добавленным полем 'avatar_path'
    """
    profile = get_tiktok_profile(username)
    if not profile:
        return None

    avatar_path = download_avatar(profile['avatar_url'], username)
    profile['avatar_path'] = avatar_path

    return profile


def get_tiktok_profile(username: str):
    url = f"https://www.tiktok.com/{username}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    response = requests.get(url, headers=headers, timeout=30)
    html_content = response.text
    return extract_tiktok_data(html_content)

def extract_tiktok_data(html_content):
    """
    Извлекает ID пользователя, имя пользователя (uniqueId), никнейм (nickname)
    и URL аватара со страницы TikTok.

    :param html_content: Строка, содержащая HTML-код страницы TikTok.
    :return: Словарь с данными пользователя или None, если данные не найдены.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Ищем скрипт с данными для гидрации
    script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__')

    if not script_tag:
        print("Тег <script id='__UNIVERSAL_DATA_FOR_REHYDRATION__'> не найден.")
        return None

    try:
        data = json.loads(script_tag.string)
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON из содержимого тега <script>.")
        return None

    # Извлекаем информацию о пользователе со страницы
    # Обычно информация о пользователе, чей профиль мы просматриваем,
    # находится в __DEFAULT_SCOPE__ -> webapp.user-detail -> userInfo -> user
    try:
        user_info_container = data.get("__DEFAULT_SCOPE__", {}).get("webapp.user-detail", {})
        if not user_info_container: # Пробуем другой возможный путь, если первый пуст
            user_info_container = data.get("webapp.user-detail", {})

        user_data = user_info_container.get("userInfo", {}).get("user", {})

        if not user_data:
            print("Данные пользователя (webapp.user-detail.userInfo.user) не найдены в JSON.")
             # Попытка найти данные в другом месте, если страница авторизованного пользователя
            app_context_user = data.get("__DEFAULT_SCOPE__", {}).get("webapp.app-context", {}).get("user", {})
            if app_context_user and 'uid' in app_context_user:
                 user_id = app_context_user.get("uid")
                 user_name = app_context_user.get("uniqueId")
                 last_name = app_context_user.get("nickName") # В TikTok это никнейм
                 avatar_url = app_context_user.get("avatarUri", [None])[0] # Берем первую ссылку, если есть
                 print("Найдены данные из webapp.app-context.user (возможно, это данные залогиненного пользователя)")
                 return {
                    "id": user_id,
                    "username": user_name,
                    "nickname": last_name,
                    "avatar_url": avatar_url
                }
            return None


        user_id = user_data.get("id")
        user_name = user_data.get("uniqueId")
        last_name = user_data.get("nickname") # В TikTok это никнейм
        avatar_url = user_data.get("avatarLarger") # Используем avatarLarger для лучшего качества

        if not all([user_id, user_name, last_name, avatar_url]):
             print("Не все требуемые поля найдены в webapp.user-detail.userInfo.user:")
             print(f"  ID: {user_id}, Username: {user_name}, Nickname: {last_name}, Avatar: {avatar_url}")


        return {
            "id": user_id,
            "username": user_name,
            "nickname": last_name,
            "avatar_url": avatar_url
        }

    except KeyError as e:
        print(f"Ключ не найден в JSON: {e}")
        return None
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при извлечении данных: {e}")
        return None
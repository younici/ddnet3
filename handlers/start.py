from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import data_base as db
import datetime

router = Router()
COMMANDS='''
/help - список команд
/r @<ttusername> - регистрация в списке чата
/u @<ttusername> - обновить имя
/users - отображения списка пользователей
/userinfo - для просмотра информации о пользователе, для использования нужно ответить на сообщение этой командой или ввести айди пользователя
/dellme - удалить себя из базы данных (списка тик токеров)
/search @<ttusername> - (можно без @ и написать основную часть имени) поиск пользователя в списке чата\n
для админов:
/delluser <id> - даляет пользователя из базы данных
/admr @<ttusername> <id> - регистрация пользователей которые сами не добавили свой ник
/UMT <text> - обновить сообщение об автоматических обновлениях
/UMS <status> (1 или 0) - задать статус отправки сообщения об автоматических обновлениях базы данных
/CD <second> - задать кулдаун для команды /users
/updateDB - запустить скрип обновления базы данных
/UsersLink <link> - задать ссылку на таблицу
'''


@router.message(Command('start'))
async def start_command(message: Message):
    await message.reply('введите команду /help для помощи')

@router.message(Command('help'))
async def help_command(message: Message):
    if db.check_user_cooldown(message.from_user.id) is False:
        await message.reply(COMMANDS)
        db.set_user_last_time_use_command(message.from_user.id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        await message.reply("вы слишком часто используете эту команду")
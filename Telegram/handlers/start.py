from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()
COMMANDS='''
/help - список команд
/r @<ttusername> - регистрация в списке чата
/u @<ttusername> - обновить имя
/users - ссылка на сайт с списком пользователей
/userinfo - для просмотра информации о пользователе, для использования нужно ответить на сообщение этой командой или ввести айди пользователя
/dellme - удалить себя из базы данных (списка тик токеров)
/search @<ttusername> - (можно без @ и написать основную часть имени) поиск пользователя в списке чата\n
для админов:
/up <id - или ответ на сообщение пользователя этой командой> - назначить пользователя админом
/down <id - или ответ на сообщение пользователя этой командой> - снять админа
/delluser <id> - удаляет пользователя из базы данных
/admr @<ttusername> <id> - регистрация пользователей которые сами не добавили свой ник или для обновления ника
/UMT <text> - обновить сообщение об автоматических обновлениях
/UMS <status> (1 или 0) - задать статус отправки сообщения об автоматических обновлениях базы данных
/updateDB - запустить скрип обновления базы данных
/UsersLink <link> - задать ссылку на таблицу
'''


@router.message(Command('start'))
async def start_command(message: Message):
    await message.reply('введите команду /help для помощи')

@router.message(Command('help'))
async def help_command(message: Message):
    await message.reply(COMMANDS)
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from queries import hero

msg_for_help = r'''
Вас приветствует Dota Stats Bot.

Справка по использованию бота:

Основные понятия:
{hero} -  имя героя: аргумент, принимающий как официальное имя героя (Anti-Mage), так же устоявшиеся в коммьюнити сокращения (am, valora, furion)
{patch} - минимальный номер патча: аргумент, принимающий номер патча без букв и разделителем в виде точки (7.32, 7.31 и тд)
(tier_level) - уровень игр при учёте статистики: "professional": t1-t4, "premium": только t1
{player_name} - имя игрока: принимает только официальный формат (temel для TorontoTokyo не подойдет)

Шаблон: "/команда {аргументы}"

/hero {hero} {patch} {tier_level} - команда возвращает статистику по герою.
Отсчет статистики идет от номера патча (дефолтное значение 7.32), также можно задать 
'''


################### USER HANDLERS
async def help_command(message : types.Message):
    await message.reply(msg_for_help)

async def heroes_command(message : types.Message):
    await message.reply(message.get_args())

def register_user_commands(dispatcher : Dispatcher):
    dispatcher.register_message_handler(help_command, Command(commands=['help']))
    dispatcher.register_message_handler(heroes_command, Command(commands=['heroes']))
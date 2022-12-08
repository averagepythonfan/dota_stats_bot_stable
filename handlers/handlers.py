import aiohttp
import logging
import pandas
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from queries import hero, heroes, hero_with_hero, player
from os import getcwd
from time import ctime

#set logging
logging.basicConfig(level='DEBUG', filename=f'{getcwd()}/dotastatsbotlog.log')
logger = logging.getLogger(__name__)
logging.getLogger('aiohttp').setLevel('ERROR')
logging.getLogger('aiogram').setLevel('ERROR')
logging.getLogger('pandas').setLevel('ERROR')



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

async def hero_command(message : types.Message):
    pass

async def heroes_command(message : types.Message):
    await message.reply(message.get_args())

async def hero_with_command(message : types.Message):
    pass

async def hero_against_command(message : types.Message):
    pass

async def player_command(message : types.Message):
    pass

async def winrate_wilson_command(message : types.Message):
    pass

#admin handlers
async def update_player_command(message : types.Message): #TEST SUCCESSFULLY
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.opendota.com/api/proPlayers') as resp:
            if resp.status == 200:
                response = await resp.json()
                df = pandas.DataFrame(response)
                df.to_csv('players.csv', index=False)
                logger.debug(f'Update players db at {ctime()}')
                await message.reply('Player db updated!')
            else:
                logger.warning(f'Player db update failed at {ctime()}')
                await message.reply('FAILED')


#register all commands
def register_user_commands(dispatcher : Dispatcher):
    dispatcher.register_message_handler(help_command, Command(commands=['help']))
    dispatcher.register_message_handler(hero_command, Command(commands=['hero']))
    dispatcher.register_message_handler(heroes_command, Command(commands=['heroes']))
    dispatcher.register_message_handler(hero_with_command, Command(commands=['hero_with']))
    dispatcher.register_message_handler(hero_against_command, Command(commands=['hero_againts']))
    dispatcher.register_message_handler(player_command, Command(commands=['player']))
    dispatcher.register_message_handler(winrate_wilson_command, Command(commands=['winrate_wilson']))
    dispatcher.register_message_handler(update_player_command, Command(commands=['update_players']))
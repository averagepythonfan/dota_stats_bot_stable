import aiohttp
import logging
import pandas
import numpy
import dataframe_image as dfi
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from queries import hero, heroes, hero_with_hero, player
from os import getcwd, remove
from time import ctime, time

#set logging
logging.basicConfig(level='DEBUG', filename=f'{getcwd()}/dotastatsbotlog.log')
logger = logging.getLogger(__name__)
logging.getLogger('aiohttp').setLevel('ERROR')
logging.getLogger('aiogram').setLevel('ERROR')
logging.getLogger('pandas').setLevel('ERROR')
logging.getLogger('matplotlib').setLevel('ERROR')



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

async def heroes_command(message : types.Message, patch=7.32, tier_level='premium'):
    '''Отправляет дата фрейм с 10 лучшими и 10 худщими героями патча.

    Параметр: patch - минимальный патч для отсчета статистики герое. Дефолтное значение 7.32
    Параметр: tier_level - уровень игры для сбора статистики. Доступные значения premuin и professional.
    '''
    args = ['start']
    if len(message.get_args().split()) == 1:
        args = message.get_args().split()
        patch = float(args[0])
    elif len(message.get_args().split()) == 2:
        args = message.get_args().split()
        patch = float(args[0])
        tier_level = args[1]

    if args[0] == 'help':
        message.reply(heroes_command.__doc__)
    else:
        await message.reply('Wait, i\'m working')
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.opendota.com/api/explorer', params=dict(sql=heroes.format(patch=patch, tier_level=tier_level))) as resp:
                if resp.status == 200:
                    query = await resp.json()
                    df = pandas.DataFrame(query['rows'])
                    df = df.iloc[:, :5]
                    df = df.rename(columns={'localized_name' : 'name', 'AVG Kills' : 'avg_kills', 'winrate_wilson' : 'win_wil', 'count' : 'matches'})

                    df.win_wil = numpy.round(df.win_wil.values, 2) * 100
                    df.avg_kills = numpy.round(df.avg_kills.values.astype(float), 2)
                    df.winrate = numpy.round(df.winrate.values, 4) * 100

                    df = df[(df.matches > 30)].sort_values(by=['win_wil'], ascending=False)
                    df = pandas.concat([df.head(10), df.tail(10)])
                    df = df.reset_index(drop=True)

                    indx = round(time())
                    dfi.export(df, f'mytable{indx}.png', table_conversion='matplotlib')
                    df_pic = types.InputFile(f'{getcwd()}/mytable{indx}.png')
                    await message.reply_photo(df_pic)
                    remove(f'mytable{indx}.png')
                    logger.debug(f'Heroes df pic send to {message.from_user.id}, username {message.from_user.username} at {ctime()}')
                else:
                    await message.reply('Try again!')
                    logger.warning(f'Response equals {resp.status}')

    # path_file = types.InputFile('/home/eugene/Coding/dataframe_image/mytable1670520517.png')
    # #onswer = path.exists(path_file)
    # #logger.info(f'Answer is {onswer}')
    # await message.reply_photo(path_file)

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
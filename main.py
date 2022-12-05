import os
import asyncio
from config import TOKEN, ADMIN_ID
from handlers import bot_commands

from aiogram import Dispatcher, Bot
from aiogram import types

async def main():

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(types.BotCommand(command=cmd[0], description=cmd[1]))


    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
    await bot.set_my_commands(commands=commands_for_bot)

    await dp.start_polling()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')
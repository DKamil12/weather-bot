import asyncio
import sys
import logging
from aiogram import Dispatcher, Bot
from handlers import start, weather

TOKEN = ''

async def run():
    bot = Bot(TOKEN)
    dp = Dispatcher()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    dp.include_routers(start.router, weather.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run())
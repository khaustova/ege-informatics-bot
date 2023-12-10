import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage, Redis
from configuration import config
from handlers import common

logging.basicConfig(level=logging.INFO)


async def main():
    redis = Redis(host='localhost', port=6379, db=0)
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)
    dp.include_routers(common.router)
    
    bot = Bot(token=config.bot.token)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
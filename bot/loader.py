from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from bot.configuration import config
from bot.handlers import common

redis = Redis(host='localhost', port=6379, db=0)
storage = RedisStorage(redis=redis)

dp = Dispatcher(storage=storage)
bot = Bot(token=config.bot.token)

dp.include_routers(common.router)

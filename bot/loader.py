from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from .configuration import config

redis = Redis(
    host=config.redis.host, 
    port=config.redis.port, 
    db=0
)
storage = RedisStorage(redis=redis)

dp = Dispatcher(storage=storage)
bot = Bot(token=config.bot.token)

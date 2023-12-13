import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from bot.configuration import config
from bot.handlers import user_handlers
from bot.handlers import admin_handlers
from bot.keyboards.set_menu import set_main_menu

redis = Redis(host='localhost', port=6379, db=0)
storage = RedisStorage(redis=redis)

dp = Dispatcher(storage=storage)
bot = Bot(token=config.bot.token)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )
    
    dp.include_routers(user_handlers.router, admin_handlers.router)
    
    await set_main_menu(bot)
    
    await dp.start_polling(bot)
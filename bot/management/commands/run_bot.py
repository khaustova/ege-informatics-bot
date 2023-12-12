import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from django.core.management.base import BaseCommand
from bot.configuration import config
from bot.handlers import common
from bot.loader import dp, bot


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        help = 'Starts a bot.'
        
        async def main():
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            )
            await dp.start_polling(bot)
            
        asyncio.run(main())

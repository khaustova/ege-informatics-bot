import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from django.core.management.base import BaseCommand
from bot.configuration import config
from bot.handlers import user_handlers
from bot.main import main


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        help = 'Starts a bot.'
                  
        asyncio.run(main())

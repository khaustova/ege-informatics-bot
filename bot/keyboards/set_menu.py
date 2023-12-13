from aiogram import Bot
from aiogram.types import BotCommand


LEXICON_COMMANDS_RU: dict[str, str] = {
    '/admin': 'command_1 desription',
    '/start': 'command_2 desription',
}

# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS_RU.items()
    ]
    await bot.set_my_commands(main_menu_commands)
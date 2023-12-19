import logging
from .loader import bot, dp
from .keyboards.commands_menu import set_commands_menu
from .handlers import exam_handlers, menu_handlers, admin_handlers


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )
    
    dp.include_routers(
        exam_handlers.router, 
        menu_handlers.router, 
        admin_handlers.router
    )
    
    await set_commands_menu(bot)
    
    await dp.start_polling(bot)
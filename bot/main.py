import logging
from .loader import bot, dp
from .keyboards.commands_menu import set_commands_menu
from .handlers import exam_handlers, menu_handlers, statistics_handlers, admin_handlers, about_handlers


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        #filename='logs/bot.log',filemode='w',
        format='%(asctime)s: %(levelname)s - %(name)s - %(message)s',
    )
    
    
    dp.include_routers(
        admin_handlers.router,
        statistics_handlers.router,
        about_handlers.router,
        menu_handlers.router, 
        exam_handlers.router, 
    )
    
    await set_commands_menu(bot)
    
    await dp.start_polling(bot)
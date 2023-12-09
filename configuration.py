from dataclasses import dataclass
from os import getenv


@dataclass
class BotConfig:
    token: str = getenv('BOT_TOKEN')
    
    
@dataclass
class Configuration:
    bot = BotConfig
    

config = Configuration()
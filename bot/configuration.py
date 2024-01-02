from dataclasses import dataclass
from os import getenv

@dataclass
class BotConfig:
    token: str = getenv('BOT_TOKEN')
    
    
@dataclass
class RedisConfig:
    host: str = getenv('REDIS_HOST')
    port: int = getenv('REDIS_PORT')
    
@dataclass
class Configuration:
    bot = BotConfig
    redis = RedisConfig
    


config = Configuration()
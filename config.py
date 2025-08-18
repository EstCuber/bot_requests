# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# BOT_TOKEN = os.getenv('BOT_TOKEN')
# ADMIN_ID = os.getenv('ADMIN_ID')
# DB_URL = os.getenv('DB_URL')

from pydantic_settings import BaseSettings, SettingsConfigDict
import logging.config

def setup_logging() -> None:
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'DEBUG',
                'stream': 'ext://sys.stdout',
            },            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'level': 'INFO',
                'filename': 'bot.log',
                'mode': 'w',
            }        },        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }   }
    logging.config.dictConfig(LOGGING_CONFIG)


class Settings(BaseSettings):
    BOT_TOKEN: str
    #ADMIN_ID: int
    #DB_URL: str
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
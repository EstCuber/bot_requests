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
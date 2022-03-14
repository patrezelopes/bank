import logging.config
from functools import lru_cache

from pydantic import BaseSettings, AmqpDsn, AnyUrl


class ConfigDefault(BaseSettings):
    CELERY_BROKER_URL: AmqpDsn = "amqp://guest:guest@localhost:5672"
    OPERATIONS_HOST: AnyUrl = "http://localhost:8000"
    API_KEY: str = None
    AUTHORIZATION: str = None
    BROKER_HOST: str = "localhost"
    BROKER_USER: str = "guest"
    BROKER_PASS: str = "guest"
    BROKER_PORT: int = 5672
    QUEUE: str = "events_queue"
    ROUTING_KEY: str = "events"

    # class Config:
    #     env_file = ".env"


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%s'
        }
    },
    'handlers': {
        'dev_null': {
            'class': 'logging.NullHandler'
        },
        'stdout_logger': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        },
    },
    'loggers': {
        'logger': {
            'level': "INFO",
            'handlers': ['stdout_logger'],
            'propagate': False,
        },
    },
}


@lru_cache(maxsize=128)
def get_config():
    return ConfigDefault()


logging.config.dictConfig(LOGGING)

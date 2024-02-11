import os
from dotenv import load_dotenv
import logging

from app.common.error import InternalError

load_dotenv()


class Config:
    version = "0.1.0"
    title = "UserVote API"

    app_settings = {
        'db_name': os.getenv('MONGO_DB'),
        'mongodb_url': os.getenv('MONGO_URL'),
        'mongo_username': os.getenv('MONGO_HOSTED_USERNAME'),
        'mongo_password': os.getenv('MONGO_HOSTED_PASSWORD'),
        'max_db_conn_count': os.getenv('MAX_CONNECTIONS_COUNT'),
        'min_db_conn_count': os.getenv('MIN_CONNECTIONS_COUNT'),
    }

    @classmethod
    def validate_app_settings(cls):
        for k, v in cls.app_settings.items():
            if v is None:
                logging.error(f'Config variable error. {k} cannot be None')
                raise InternalError([{"message": "Server configure error"}])
            else:
                logging.info(f'Config variable {k} is {v}')

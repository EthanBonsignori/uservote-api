from dotenv import load_dotenv
from motor.core import AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient
import logging

from app.config.config import Config

load_dotenv()

db_client: AgnosticDatabase = None


async def get_database_client() -> AgnosticDatabase:
    return db_client


async def connect_and_init_db():
    global db_client
    logging.info('Connecting to mongo...')
    mongo_username = Config.app_settings.get('mongo_username')
    mongo_password = Config.app_settings.get('mongo_password')
    db_name = Config.app_settings.get('db_name')

    uri = f"mongodb+srv://{mongo_username}:{
        mongo_password}@{db_name}.tbmgy3w.mongodb.net/?retryWrites=true&w=majority"
    try:
        db_client = AsyncIOMotorClient(
            uri,
            maxPoolSize=Config.app_settings.get('max_db_conn_count'),
            minPoolSize=Config.app_settings.get('min_db_conn_count'),
            uuidRepresentation="standard",
        )
        db_client.admin.command('ping')
        logging.info('Connected to MongoDB!')
    except Exception as e:
        logging.exception(f'Could not connect to mongo: {e}')
        raise


async def close_db_connect():
    global db_client
    if db_client is None:
        logging.warning('Connection is None, nothing to close.')
        return
    db_client.close()
    db_client = None
    logging.info('Mongo connection closed.')

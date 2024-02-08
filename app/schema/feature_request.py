from uuid import uuid4, UUID
from datetime import datetime
from pymongo import ReturnDocument

import logging
from app.config.config import Config
from app.database.database import AsyncIOMotorClient
from app.models.feature_request import FeatureRequest
from app.common.utils import uuid_masker


__db_name = Config.app_settings.get('db_name')
__db_collection = 'feature_request'


async def create_feature_request(
    conn: AsyncIOMotorClient,
    title: str,
    content: str,
    author_username: str
) -> FeatureRequest:
    new_feature_request = FeatureRequest(
        id=uuid4(),
        title=title,
        content=content,
        author_username=author_username,
        category="requested",
        comments=[],
        votes=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        deleted=False,
    )
    logging.info(
        f'Inserting feature request {title} into db...'
    )
    await conn[__db_name][__db_collection].insert_one(
        new_feature_request.mongo()
    )
    logging.info(
        f"Sample resource {title} has inserted into db"
    )
    return new_feature_request


async def get_feature_requests(
    conn: AsyncIOMotorClient,
) -> list | None:
    logging.info(f"Getting all feature requests...")
    feature_requests = conn[__db_name][__db_collection].find(
        {"deleted": {"$ne": True}})
    feature_requests_list = await feature_requests.to_list(length=100)
    if None is feature_requests:
        logging.info(f"Feature requests are None")
    return feature_requests_list


async def get_feature_request_by_id(
    conn: AsyncIOMotorClient,
    resource_id: UUID
) -> FeatureRequest | None:
    logging.info(f"Getting feature request {uuid_masker(resource_id)}...")
    feature_request = await conn[__db_name][__db_collection].find_one(
        {"$and": [
            {'_id': resource_id},
            {'deleted': False},
        ]},
    )
    if None is feature_request:
        logging.info(f"Feature request {uuid_masker(resource_id)} is None")
    return feature_request


async def update_feature_request(
    conn: AsyncIOMotorClient,
    resource_id: UUID,
    resource_data: dict
) -> FeatureRequest | None:
    logging.info(
        f'Updating feature request {uuid_masker(str(resource_id))}...'
    )
    feature_request = await conn[__db_name][__db_collection].find_one_and_update(
        {"$and": [
            {'_id': resource_id},
            {'deleted': False},
        ]},
        {'$set': {
            **resource_data,
            "updated_at": datetime.utcnow(),
        }},
        return_document=ReturnDocument.AFTER,
    )
    if None is feature_request:
        logging.error(
            f"Feature request {uuid_masker(str(resource_id))} is None"
        )
    else:
        logging.info(
            f'Feature request {uuid_masker(str(resource_id))} updated'
        )
    return feature_request


async def delete_feature_request(
    conn: AsyncIOMotorClient,
    resource_id: UUID,
) -> FeatureRequest | None:
    logging.info(
        f"Deleting feature request {uuid_masker(str(resource_id))}..."
    )

    feature_request = await conn[__db_name][__db_collection].\
        find_one_and_update(
        {"$and": [
            {'_id': resource_id},
            {'deleted': False},
        ]},
        {'$set': {
            "deleted": True,
            "updated_at": datetime.utcnow(),
        }},
        return_document=ReturnDocument.AFTER,
    )

    if None is feature_request:
        logging.error(
            f"Feature request {uuid_masker(str(resource_id))} is None"
        )
    else:
        logging.info(
            f'Feature request {uuid_masker(str(resource_id))} deleted'
        )
    return feature_request

from fastapi import APIRouter, Depends, Response
from uuid import UUID

import logging
from app.database.database import get_db, AsyncIOMotorClient
from app.common.utils import uuid_masker
from app.common.error import UnprocessableError
from app.schema.feature_request import \
    get_feature_requests as db_get_feature_requests, \
    get_feature_request_by_id as db_get_feature_request_by_id, \
    create_feature_request as db_create_feature_request, \
    update_feature_request as db_update_feature_request, \
    delete_feature_request as db_delete_feature_request

from app.models.feature_request import FeatureRequestCreateRequest, FeatureRequestGetResponse, FeatureRequestCreateResponse

router = APIRouter()


@router.get('/', include_in_schema=False, status_code=200)
@router.get('', response_model=list, status_code=200, responses={400: {}})
async def get_feature_requests(
    db: AsyncIOMotorClient = Depends(get_db),
):
    logging.info('Received get feature requests request')

    feature_requests = await db_get_feature_requests(db)

    if None is feature_requests:
        return Response(status_code=404)

    return feature_requests


@router.get('/{id}', include_in_schema=False, status_code=200)
@router.get('/{id}', response_model=FeatureRequestGetResponse, status_code=200, responses={400: {}})
async def get_feature_request_by_id(
    id: UUID,
    db: AsyncIOMotorClient = Depends(get_db),
):
    logging.info(
        f'Received get feature request {uuid_masker(id)} request'
    )

    feature_request = await db_get_feature_request_by_id(
        db,
        id
    )

    if None is feature_request:
        return Response(status_code=404)

    return FeatureRequestGetResponse(
        id=feature_request.get("_id"),
        created_at=feature_request.get("created_at"),
        updated_at=feature_request.get("updated_at"),
        title=feature_request.get("title"),
        content=feature_request.get("content"),
        votes=feature_request.get("votes"),
        category=feature_request.get("category"),
        author_username=feature_request.get("author_username"),
        comments=feature_request.get("comments"),
    )


@router.post('/', include_in_schema=False, status_code=201)
@router.post('', response_model=FeatureRequestCreateResponse, status_code=201, responses={400: {}})
async def create_feature_request(
    feature_request_data: FeatureRequestCreateRequest,
    db: AsyncIOMotorClient = Depends(get_db)
):
    logging.info('Received create feature request request')

    # TODO: return actual document, not the user's input
    feature_request_db = await db_create_feature_request(
        db,
        feature_request_data.title,
        feature_request_data.content,
        feature_request_data.author_username
    )

    return FeatureRequestCreateResponse(id=feature_request_db.id)


@router.put('/{id}', include_in_schema=False, status_code=200)
@router.put('/{id}', status_code=200, responses={400: {}})
async def update_sample_resource(
    id: UUID,
    feature_request_data: FeatureRequestCreateRequest,
    db: AsyncIOMotorClient = Depends(get_db),
):
    logging.info(
        f'Received update feature request {uuid_masker(id)} request'
    )

    feature_request_db = await db_update_feature_request(
        db,
        id,
        feature_request_data.model_dump()
    )
    if None is feature_request_db:
        raise UnprocessableError([])

    return FeatureRequestCreateResponse(id=feature_request_db.get("_id"))


@router.delete('/{id}', include_in_schema=False, status_code=200)
@router.delete('/{id}', status_code=200, responses={400: {}})
async def delete_feature_request(
    id: UUID,
    db: AsyncIOMotorClient = Depends(get_db),
):
    logging.info(
        f'Received delete feature request {uuid_masker(id)} request'
    )

    feature_request_db = await db_delete_feature_request(
        db,
        id,
    )
    if None is feature_request_db:
        raise UnprocessableError([])
    return Response(status_code=204)

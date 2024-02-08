from fastapi import APIRouter, Depends, Response
from uuid import UUID

import logging
from app.database.database import get_db, AsyncIOMotorClient
from app.common.utils import uuid_masker
from app.common.error import UnprocessableError
from app.schema.feature_request import \
    get_feature_request as db_get_feature_request, \
    create_feature_request as db_create_feature_request, \
    update_feature_request as db_update_feature_request, \
    delete_feature_request as db_delete_feature_request

from app.models.feature_request import FeatureRequestCreateRequest, FeatureRequestGetResponse, FeatureRequestCreateResponse

router = APIRouter()


@router.get('/', include_in_schema=False, status_code=200)
@router.get('', response_model=FeatureRequestGetResponse, status_code=200, responses={400: {}})
async def get_feature_request(
    resource: UUID,
    db: AsyncIOMotorClient = Depends(get_db),
):
    logging.info(
        f'Received get feature request {uuid_masker(resource)} request'
    )

    feature_request = await db_get_feature_request(
        db,
        resource
    )

    if None is feature_request:
        return Response(status_code=204)

    return FeatureRequestGetResponse(
        title=feature_request.get("title"),
        content=feature_request.get("content"),
        votes=feature_request.get("votes"),
        category=feature_request.get("category"),
        author_id=feature_request.get("author_id"),
        author_username=feature_request.get("author_username"),
        comments=feature_request.get("comments")
    )


@router.post('/', include_in_schema=False, status_code=201)
@router.post('', response_model=FeatureRequestCreateResponse, status_code=201, responses={400: {}})
async def create_feature_request(
    feature_request_data: FeatureRequestCreateRequest,
    db: AsyncIOMotorClient = Depends(get_db)
):
    logging.info('Received create feature request request')

    feature_request_db = await db_create_feature_request(
        db,
        feature_request_data.title,
        feature_request_data.content,
        feature_request_data.author_username
    )

    return FeatureRequestCreateResponse(id=feature_request_db.id)


# @app.get("/api/posts")
# async def get_all_posts():
#     documents = []
#     cursor = posts_collection.find({})
#     async for document in cursor:
#         documents.append(Post(**document))
#     if not documents:
#         raise HTTPException(404, "No posts found")
#     return documents


# @app.get("/api/posts/{id}")
# async def get_post_by_id(id: str):
#     response = await posts_collection.find_one({"_id": ObjectId(id)})
#     if not response:
#         raise HTTPException(404, "Post not found")
#     return response


# @app.post("/api/posts", response_model=Post)
# async def create_post(postTitle: str, postContent: str, user_id: int, username: str):
#     today = datetime.datetime.today().replace(microsecond=0)
#     post: Post = {
#         "_id": str(ObjectId()),
#         "created_at": today,
#         "updated_at": today,
#         "title": postTitle,
#         "content": postContent,
#         "votes": 0,
#         "category": "requested",
#         "author_id": user_id,
#         "author_username": username,
#         "comments": []
#     }
#     result = await posts_collection.insert_one(post)
#     if not result.inserted_id:
#         raise HTTPException(500, "Internal Server Error")
#     response = await posts_collection.find_one({"_id": result.inserted_id})
#     if not response:
#         raise HTTPException(404, "Post not found")
#     return response


# @app.put("/api/posts/{id}")
# async def update_post_by_id(id: str, post: Post):
#     document = Post({
#         **post,
#         "updated_at": datetime.datetime.today().replace(microsecond=0)
#     })
#     result = await posts_collection.update_one({"_id": id}, {"$set": document})
#     if not result.modified_count == 1:
#         raise HTTPException(404, "Post not found")
#     response = await posts_collection.find_one({"_id": id})
#     if not response:
#         raise HTTPException(404, "Post not found")
#     return response


# @app.delete("/api/posts/{id}")
# async def delete_post_by_id(id: int):
#     response = await posts_collection.delete_one({"_id": id})
#     if not response.deleted_count == 1:
#         raise HTTPException(404, "Post not found")
#     return response.deleted_count

from models.post import Post

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")

database = client.UserVote
post_collection = database.post
user_collection = database.user

async def find_all_posts():
    documents = []
    cursor = post_collection.find({})
    async for document in cursor:
        documents.append(Post(**document))
    return documents

async def find_one_post(id: int):
    document = await post_collection.find_one({"_id": id})
    return document

async def insert_post(post: Post):
    document = post
    result = await post_collection.insert_one(document)
    return result

async def update_post(id: int, post: Post):
    document = post
    result = await post_collection.update_one({"_id": id}, {"$set": document})
    return result

async def delete_post(id: int):
    result = await post_collection.delete_one({"_id": id})
    return result
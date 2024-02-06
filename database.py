from models import post
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
database = client.UserFeedback
collection = database.posts

async def find_one_post(id: int):
    document = await collection.find_one({"id": id})
    return document

async def find_all_posts():
    documents = collection.find({})
    return [document async for document in documents]

async def create_post(new_post: post):
    document = new_post.dict()
    result = await collection.insert_one(document)
    return result

async def update_post(id: int, new_post: post):
    document = new_post.dict()
    result = await collection.update_one({"id": id}, {"$set": document})
    return result

async def delete_post(id: int):
    result = await collection.delete_one({"id": id})
    return result
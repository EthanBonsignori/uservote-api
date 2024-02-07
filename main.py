import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.post import Post

from database import (
    find_all_posts,
    find_one_post,
    insert_post,
    update_post,
    delete_post
)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/posts")
async def get_all_posts():
    response = await find_all_posts()
    if response:
        return response
    raise HTTPException(404, "No posts found")


@app.get("/api/posts/{id}")
async def get_post_by_id(id: int):
    response = await find_one_post(id)
    if response:
        return response
    raise HTTPException(404, "Post not found")

@app.post("/api/posts")
async def create_post(postTitle: str, postContent: str, user_id: int, username: str):
    today = datetime.datetime.today().replace(microsecond=0)
    response = await insert_post({
        "created_at": today,
        "updated_at": today,
        "title": postTitle,
        "content": postContent,
        "author_id": user_id,
        "author_username": username,
        "votes": 0,
        "category": "requested"
    })
    if response:
        return response
    raise HTTPException(500, "Internal Server Error")

@app.put("/api/posts/{id}")
async def update_post_by_id(id: int, post: Post):
    response = await update_post(id, {
       **post,
       "updated_at": datetime.datetime.today().replace(microsecond=0)
    })
    if response:
        return response
    raise HTTPException(404, "Post not found")

@app.delete("/api/posts/{id}")
async def delete_post_by_id(id: int):
    response = await delete_post(id)
    if response:
        return response
    raise HTTPException(404, "Post not found")


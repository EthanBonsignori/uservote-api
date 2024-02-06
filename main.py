from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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
async def get_posts():
    return 1

@app.get("/api/posts/{id}")
async def get_post(id: int):
    return {"id": id}

@app.post("/api/posts")
async def create_post():
    return 1

@app.put("/api/posts/{id}")
async def update_post(id: int):
    return {"id": id}

@app.delete("/api/posts/{id}")
async def delete_post(id: int):
    return {"id": id}


from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    username: str
    voted_posts: set[int]
    created_posts: set[int]
    created_comments: set[int]
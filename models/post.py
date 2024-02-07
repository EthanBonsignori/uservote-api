from enum import Enum
from datetime import datetime
from pydantic import BaseModel

from models.comment import Comment

class Category(Enum):
    REQUESTED = "requested"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    WONT_DO = "wont_do"
    RELEASED = "released"

class Post(BaseModel):
    created_at: datetime
    updated_at: datetime
    title: str
    content: str
    votes: int
    category: Category = Category.REQUESTED
    author_id: int
    author_username: str
    comments: list[Comment] = []
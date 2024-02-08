from pydantic import BaseModel
from datetime import datetime


class Comment(BaseModel):
    created_at: datetime
    updated_at: datetime
    content: str
    author_username: str

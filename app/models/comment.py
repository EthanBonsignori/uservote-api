from pydantic import BaseModel
from datetime import datetime

class Comment(BaseModel):
    created_at: datetime
    updated_at: datetime
    content: str
    author_id: int
    author_username: str
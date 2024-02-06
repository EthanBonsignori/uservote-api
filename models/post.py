import enum
from pydantic import BaseModel

class Category(enum.Enum):
    REQUESTED = "requested"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    WONT_DO = "wont_do"
    RELEASED = "released"

#todo
# class Comment(BaseModel):
#     id: int
#     content: str
#     user: id

class Post(BaseModel):
    id: int
    title: str
    content: str
    votes: int
    category: Category
    #todo
    # comments: list[]
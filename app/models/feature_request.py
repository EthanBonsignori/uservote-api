from enum import Enum
from datetime import datetime
from uuid import UUID
from typing_extensions import Annotated

from app.common.utils import to_lower_camel_case
from .mongo_model import MongoModel
from .comment import Comment


class Category(Enum):
    REQUESTED = "requested"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    WONT_DO = "wont_do"
    RELEASED = "released"


class FeatureRequestBase(MongoModel):
    title: str
    content: str
    votes: int = 0
    category: Category = Category.REQUESTED
    author_username: str
    comments: list[Comment] = []


class FeatureRequestDB(FeatureRequestBase, MongoModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted: bool


class FeatureRequestCreateRequest(FeatureRequestBase):
    class Config:
        alias_generator: to_lower_camel_case


class FeatureRequestCreateResponse(FeatureRequestBase):
    id: UUID


class FeatureRequestGetResponse(MongoModel):
    title: str
    content: str
    votes: int
    category: Category = Category.REQUESTED
    author_id: int
    author_username: str
    comments: list[Comment] = []

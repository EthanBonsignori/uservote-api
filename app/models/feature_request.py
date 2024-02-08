from datetime import datetime
from uuid import UUID

from app.common.utils import to_lower_camel_case
from .common import MongoModel, Category
from .comment import Comment


class FeatureRequestBase(MongoModel):
    title: str
    content: str
    votes: int = 0
    category: Category = Category.REQUESTED
    author_username: str
    comments: list[Comment] = []


class FeatureRequest(FeatureRequestBase, MongoModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted: bool


class FeatureRequestCreateRequest(FeatureRequestBase):
    class Config:
        alias_generator: to_lower_camel_case


class FeatureRequestCreateResponse(MongoModel):
    id: UUID


class FeatureRequestGetResponse(MongoModel):
    id: UUID
    title: str
    content: str
    votes: int
    category: Category = Category.REQUESTED
    author_username: str
    comments: list[Comment] = []

from enum import Enum
from typing import List
from typing_extensions import Annotated

from pydantic import BaseModel, Field

UserID = Annotated[int, Field(ge=1e12, le=1e13 - 1)]
PostID = Annotated[int, Field(ge=1e12, le=1e13 - 1)]


class Metric(BaseModel):
    count: Annotated[int, Field(ge=0)]
    references: List[UserID | PostID]


class PostMetrics(BaseModel):
    likes: Metric
    shares: Metric
    comments: Metric


class Post(BaseModel):
    post_id: PostID
    author_id: UserID
    content: Annotated[str, Field(min_length=0, max_length=255)]
    metrics: PostMetrics


class UserInteraction(BaseModel):
    type: Enum('Interaction', {
        'read': 'read',
        'like': 'like',
        'share': 'share',
        'reply': 'reply'
    })
    reference: PostID


class User(BaseModel):
    user_id: UserID
    name: Annotated[str, Field(min_length=3, max_length=64)]
    following: List[UserID]
    follower: List[UserID]
    user_posts: List[Post]
    user_interactions: List[UserInteraction]

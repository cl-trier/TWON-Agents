from typing import List

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from ..schemas import UserHistory

UserID = Annotated[int, Field(ge=1e12, le=1e13 - 1)]
PostID = Annotated[int, Field(ge=1e12, le=1e13 - 1)]


class Metric(BaseModel):
    count: Annotated[int, Field(ge=0)]
    references: List[UserID | PostID]


class PostMetrics(BaseModel):
    reads: Metric
    likes: Metric
    shares: Metric
    comments: Metric


class Post(BaseModel):
    post_id: PostID
    author_id: UserID
    content: Annotated[str, Field(min_length=0, max_length=255)]
    metrics: PostMetrics


class User(BaseModel):
    user_id: UserID
    following: List[UserID]
    follower: List[UserID]
    user_posts: List[Post]
    user_history: UserHistory

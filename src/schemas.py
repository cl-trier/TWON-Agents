from enum import Enum
from typing import List

from pydantic import BaseModel


class UserActions(Enum):
    READ = 'read'
    LIKE = 'like'
    REPLY = 'reply'


class UserHistory(BaseModel):
    items: List[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                "{timestamp} - wrote the post: {content}",
                "{timestamp} - read the post: {content} by {author_id}",
                "{timestamp} - liked the post: {content} by {author_id}",
                "{timestamp} - responded the post: {content} by {author_id} with {response}",
                "[...]",
            ],
        }
    }

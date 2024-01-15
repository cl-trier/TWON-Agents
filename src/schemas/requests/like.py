from .base import BaseRequest
from .model import Post


class LikeRequest(BaseRequest):
    post: Post

    model_config = {
        "json_schema_extra": {
            "examples": [
                BaseRequest.model_config["json_schema_extra"]["examples"][0]
                | {"post": Post.model_config["json_schema_extra"]["examples"][0]}
            ]
        }
    }

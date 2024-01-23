from src.schemas import platform
from .base import BaseRequest


class LikeRequest(BaseRequest):
    post: platform.Post

    model_config = {
        "json_schema_extra": {
            "examples": [
                BaseRequest.model_config["json_schema_extra"]["examples"][0]
                | {"post": platform.Post.model_config["json_schema_extra"]["examples"][0]}
            ]
        }
    }

from src.schemas import model
from .base import BaseRequest


class LikeRequest(BaseRequest):
    post: model.Post

    model_config = {
        "json_schema_extra": {
            "examples": [
                BaseRequest.model_config["json_schema_extra"]["examples"][0]
                | {"post": model.Post.model_config["json_schema_extra"]["examples"][0]}
            ]
        }
    }

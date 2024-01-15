from .base import BaseRequest
from .model import Thread


class ReplyRequest(BaseRequest):
    thread: Thread

    model_config = {
        "json_schema_extra": {
            "examples": [
                BaseRequest.model_config["json_schema_extra"]["examples"][0]
                | {"thread": Thread.model_config["json_schema_extra"]["examples"][0]}
            ]
        }
    }

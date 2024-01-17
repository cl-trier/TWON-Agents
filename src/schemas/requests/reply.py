from typing import Literal

from .base import BaseRequest
from .model import Thread


class ReplyRequest(BaseRequest):
    thread: Thread
    length: Literal['few-word', 'single-sentence', 'short', 'long'] = 'few-word'

    model_config = {
        "json_schema_extra": {
            "examples": [
                BaseRequest.model_config["json_schema_extra"]["examples"][0]
                | {"thread": Thread.model_config["json_schema_extra"]["examples"][0], "length": "few-word"}
            ]
        }
    }

from typing import Literal

from src.schemas import platform
from .base import BaseRequest


class ReplyRequest(BaseRequest):
    thread: platform.Thread
    length: Literal['few-word', 'single-sentence', 'short', 'long'] = 'few-word'

    model_config = {
        "json_schema_extra": {
            "examples": [
                BaseRequest.model_config["json_schema_extra"]["examples"][0]
                | {"thread": platform.Thread.model_config["json_schema_extra"]["examples"][0], "length": "few-word"}
            ]
        }
    }

import typing

from src.schemas import model
from .base import BaseRequest


class ReplyRequest(BaseRequest):
    thread: model.Thread
    length: typing.Literal['few-word', 'single-sentence', 'short', 'long'] = 'few-word'

    model_config = {
        "json_schema_extra": {
            "examples": [
                BaseRequest.model_config["json_schema_extra"]["examples"][0]
                | {"thread": model.Thread.model_config["json_schema_extra"]["examples"][0], "length": "few-word"}
            ]
        }
    }

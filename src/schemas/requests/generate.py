import typing

from .base import BaseRequest


class GenerateRequest(BaseRequest):
    topic: str
    length: typing.Literal['few-word', 'single-sentence', 'short', 'long'] = 'few-word'

    model_config = {
        "json_schema_extra": {
            "examples": [
                BaseRequest.model_config["json_schema_extra"]["examples"][0]
                | {"topic": "Cookies: A round and delicious treat.", "length": "few-word"}
            ]
        }
    }

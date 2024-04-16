import typing

import pydantic

from .base import BaseRequest


class GenerateRequestOptions(pydantic.BaseModel):
    retrieve_google_news: bool = True
    include_news_src_link: bool = False


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

    options: GenerateRequestOptions = GenerateRequestOptions()

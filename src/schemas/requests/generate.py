from .base import BaseRequest


class GenerateRequest(BaseRequest):
    topic: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                BaseRequest.model_config["json_schema_extra"]["examples"][0]
                | {"topic": "Cookies: A round and delicious treat."}
            ]
        }
    }

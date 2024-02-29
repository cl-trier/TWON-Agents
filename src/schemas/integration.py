from typing import Literal

from pydantic import BaseModel


class Integration(BaseModel):
    provider: Literal['huggingFace', 'OpenAI', 'local']
    model: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "provider": "huggingFace",
                    "model": "mistralai/Mistral-7B-Instruct-v0.2",
                },
                {
                    "provider": "OpenAI",
                    "model": "gpt-3.5-turbo",
                },
                {
                    "provider": "local",
                    "model": "llama2",
                }
            ]
        }
    }

from typing import List, Literal

from pydantic import BaseModel

from .model import History
from .. import Integration, Persona


class BaseRequest(BaseModel):
    personas: List[str]
    integration: Integration = Integration.model_config["json_schema_extra"]["examples"][0]

    language: Literal['English', 'German', 'Dutch', 'Italian', 'Serbian'] = "German"
    network: Literal['Twitter', 'Reddit', 'Facebook', 'Telegram'] = "Twitter"

    history: History = []

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "personas": [
                        Persona.model_config["json_schema_extra"]["examples"][0]['id'],
                        Persona.model_config["json_schema_extra"]["examples"][1]['id'],
                    ],
                    "integration": Integration.model_config["json_schema_extra"]["examples"][0],
                    "language": "English",
                    "network": "Twitter",
                    "history": History.model_config["json_schema_extra"]["examples"][0],
                }
            ]
        }
    }

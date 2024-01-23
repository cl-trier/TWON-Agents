from typing import List, Literal

from pydantic import BaseModel

from src import schemas
from src.persona import Persona
from src.schemas import platform as ptf


class BaseRequest(BaseModel):
    personas: List[str]
    integration: schemas.Integration = schemas.Integration.model_config["json_schema_extra"]["examples"][0]

    language: Literal['English', 'German', 'Dutch', 'Italian', 'Serbian'] = "German"
    platform: Literal['Twitter', 'Reddit', 'Facebook', 'Telegram'] = "Twitter"

    history: ptf.History = []

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "personas": [
                        Persona.model_config["json_schema_extra"]["examples"][0]['id'],
                        Persona.model_config["json_schema_extra"]["examples"][1]['id'],
                    ],
                    "integration": schemas.Integration.model_config["json_schema_extra"]["examples"][0],
                    "language": "English",
                    "platform": "Twitter",
                    "history": ptf.History.model_config["json_schema_extra"]["examples"][0],
                }
            ]
        }
    }

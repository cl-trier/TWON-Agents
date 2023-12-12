from typing import List

from pydantic import BaseModel

from .history import History
from .integration import Integration
from .persona import Persona
from .thread import Thread


class AgentRequest(BaseModel):
    action: str
    personas: List[str]
    thread: Thread
    history: History
    integration: Integration = Integration.model_config["json_schema_extra"]["examples"][0]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "action": "reply",
                    "personas": [
                        Persona.model_config["json_schema_extra"]["examples"][0]['id'],
                        Persona.model_config["json_schema_extra"]["examples"][1]['id'],
                    ],
                    "thread": Thread.model_config["json_schema_extra"]["examples"][0],
                    "history": History.model_config["json_schema_extra"]["examples"][0],
                    "integration": Integration.model_config["json_schema_extra"]["examples"][0]
                }
            ]
        }
    }

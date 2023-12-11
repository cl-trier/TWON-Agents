from typing import List

from pydantic import BaseModel

from .integration import Integration
from .persona import Persona


class InteractionRequest(BaseModel):
    action: str
    personas: List[str]
    thread: str
    history: str = "You have not interacted in the thread yet."
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
                    "thread": "Post by human_user: I like cookies!\n\nReply by cookie_monster: Me Love to Eat Cookies.",
                    "history": "You have not interacted in the thread yet.",
                    "integration": Integration.model_config["json_schema_extra"]["examples"][0]
                }
            ]
        }
    }

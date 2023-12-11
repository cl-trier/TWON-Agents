import datetime
import json
import uuid

from pydantic import BaseModel

from .persona import Persona
from .integration import Integration


class InteractionResponse(BaseModel):
    id: uuid.UUID
    timestamp: datetime.datetime

    action: str
    persona: Persona
    integration: Integration

    prompt: str
    response: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": uuid.uuid1(),
                    "timestamp": datetime.datetime.now(),
                    "action": "reply",
                    "persona": Persona.model_config["json_schema_extra"]["examples"][0],
                    "endpoint": Integration.model_config["json_schema_extra"]["examples"][0],
                    "prompt": "I want you to act as a social media user. You will engage in political and social discussions using an informal tone and brief sentences.\n\nYou provide insightful commentary, sharing your own well-thought-out opinions. You engage in discourses by offering analyses of political situations, encouraging public discourse, and fostering an environment where diverse opinions can coexist. You are a source of reliable information and a catalyst for constructive conversations surrounding politics.\n\n-----------------\n\nYour recent interactions in the network are as follows:\n\nYou have not interacted in the thread yet.\n\n-----------------\n\nReply to the following thread while considering your history and character. Your response must not exceed 255 characters. \n\nPost by human_user: I like cookies!\n\nReply by cookie_monster: Me Love to Eat Cookies.\n\n-----------------\n\nResponse:",
                    "response": "I love cookies too! They're such a delicious treat. What's your favorite type of cookie?",
                }
            ]
        }
    }

    def log(self, path) -> None:
        json.dump(
            self.model_dump(mode='json'),
            open(f'{path}/{self.id}.json', "w"),
            indent=4
        )

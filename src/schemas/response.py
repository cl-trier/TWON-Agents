import datetime
import json
import re
import uuid
from typing import Literal, List

from pydantic import BaseModel

from .integration import Integration
from .persona import Persona


class Response(BaseModel):
    id: uuid.UUID = None
    timestamp: datetime.datetime = None

    action: Literal['generate', 'reply', 'like']
    persona: Persona
    integration: Integration

    prompt: str
    response: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "action": "reply",
                    "persona": Persona.model_config["json_schema_extra"]["examples"][0],
                    "endpoint": Integration.model_config["json_schema_extra"]["examples"][0],
                    "prompt": "I want you to act as a social media user. You will engage in political and social discussions using an informal tone and brief sentences.\n\nYou provide insightful commentary, sharing your own well-thought-out opinions. You engage in discourses by offering analyses of political situations, encouraging public discourse, and fostering an environment where diverse opinions can coexist. You are a source of reliable information and a catalyst for constructive conversations surrounding politics.\n\n-----------------\n\nYour recent interactions in the platform are as follows:\n\nYou have not interacted in the thread yet.\n\n-----------------\n\nReply to the following thread while considering your history and character. Your response must not exceed 255 characters. \n\nPost by human_user: I like cookies!\n\nReply by cookie_monster: Me Love to Eat Cookies.\n\n-----------------\n\nResponse:",
                    "response": "I love cookies too! They're such a delicious treat. What's your favorite type of cookie?",
                }
            ]
        }
    }

    def __init__(self, log_path: str = None, **data):
        super().__init__(**data)

        self.id = uuid.uuid1()
        self.timestamp = datetime.datetime.now()

        if self.action in ['generate', 'reply']:
            self.response = (
                re.sub(r'#\S+', '', self.response)
                .strip()
                .strip('"')
                .strip("'")
            )

        if self.action == 'like':
            choices: List[str] = re.findall(r'true|false', self.response, re.I)
            self.response = choices[0] if choices else 'false'

        if log_path:
            self.log(log_path)

    def log(self, path: str) -> None:
        json.dump(
            self.model_dump(mode='json', exclude=set('log_path')),
            open(f'{path}/{self.id}.json', "w"),
            indent=4
        )

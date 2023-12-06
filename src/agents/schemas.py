import datetime
import json
import uuid
from enum import Enum
from typing import Literal

from pydantic import BaseModel

from .data import get_agents, get_prompts

AgentID = Enum('AgentID', {agent_id: agent_id for agent_id in get_agents().keys()})
ActionID = Enum('ActionID', {action_id: action_id for action_id in get_prompts().keys()})


class AgentSchema(BaseModel):
    id: AgentID
    name: str
    icon: str
    persona: str
    summary: str

    model_config = {
        "json_schema_extra": {
            "examples": [list(get_agents().values())[0]]
        }
    }


class EndpointSchema(BaseModel):
    integration: Literal['huggingFace', 'OpenAI']
    model: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "integration": "huggingFace",
                    "model": "mistralai/Mistral-7B-Instruct-v0.1",
                },
                {
                    "integration": "OpenAI",
                    "model": "gpt-3.5-turbo",
                }
            ]
        }
    }


class AgentInteractionSchema(BaseModel):
    action: ActionID
    agent: AgentID
    thread: str
    history: str = "You have not interacted in the thread yet."
    endpoint: EndpointSchema = EndpointSchema.model_config["json_schema_extra"]["examples"][0]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "action": list(ActionID)[0],
                    "agent": list(AgentID)[0],
                    "thread": "Post by human_user: I like cookies!\n\nReply by cookie_monster: Me Love to Eat Cookies.",
                    "history": "You have not interacted in the thread yet.",
                    "endpoint": EndpointSchema.model_config["json_schema_extra"]["examples"][0]
                }
            ]
        }
    }


class AgentResponseSchema(BaseModel):
    id: uuid.UUID
    timestamp: datetime.datetime

    action: ActionID
    agent: AgentID
    endpoint: EndpointSchema

    prompt: str
    response: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": uuid.uuid1(),
                    "timestamp": datetime.datetime.now(),
                    "action": list(ActionID)[0],
                    "agent": list(AgentID)[0],
                    "endpoint": EndpointSchema.model_config["json_schema_extra"]["examples"][0],
                    "prompt": (
                        get_prompts()
                        [list(ActionID)[0].name]
                        .format(**dict(
                            persona=get_agents()[list(AgentID)[0].name]['persona'],
                            history=AgentInteractionSchema.model_config["json_schema_extra"]["examples"][0]["history"],
                            thread=AgentInteractionSchema.model_config["json_schema_extra"]["examples"][0]["thread"],
                        ))
                    ),
                    "response": "I love cookies too! They're such a delicious treat. What's your favorite type of cookie?",
                }
            ]
        }
    }

    def log(self, path) -> None:
        print(self.model_dump_json())
        json.dump(
            self.model_dump(mode='json'),
            open(f'{path}/{self.id}.json', "w"),
            indent=4
        )

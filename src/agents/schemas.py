from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from ..schemas import UserActions, UserHistory


class AgentID(Enum):
    BASE = 'base'
    AGREEING_AGENT = 'agreeing_agent'
    DISAGREEING_AGENT = 'disagreeing_agent'
    CONSPIRACY_THEORIST = 'conspiracy_theorist'
    NOBEL_PRIZE_WINNER = 'nobel_prize_winner'
    US_CONGRESS_MEMBER = 'us_congress_member'


class AgentSchema(BaseModel):
    id: AgentID
    name: str
    character: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "base",
                    "name": "🤖 Base Model",
                    "character": "",
                }
            ]
        }
    }


class AgentResponse(BaseModel):
    id: str
    prompt: str
    response: str
    model: str
    timestamp: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "hf-3ee6e358-854c-11ee-9ebb-784f439061a8",
                    "prompt": "Reply in the form of a tweet to the following text : '''I like cookies!'''",
                    "response": "\nCookies are the best! #cookie #baking #treats",
                    "model": "tiiuae/falcon-7b-instruct",
                    "timestamp": "2023-11-17T14:21:41.439198"
                }
            ]
        }
    }


class AgentInteraction(BaseModel):
    action: UserActions
    agent: AgentID
    content: Annotated[str, Field(min_length=0, max_length=255)]
    history: Optional[UserHistory] = None
    model: Optional[str] = 'Llama-2'

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "action": "reply",
                    "agent": "base",
                    "content": "I like cookies!",
                    "history": None
                }
            ]
        }
    }

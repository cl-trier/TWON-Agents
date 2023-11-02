from datetime import datetime
from enum import Enum
from typing_extensions import Annotated

from pydantic import BaseModel, Field

from ..database import get_database

AgentNames = Enum('AgentNames', {
    agent['id']: agent['id']
    for agent in list(get_database().agents.find({}))
})

AgentsActions = Enum('AgentActions', {
    template['id']: template['id']
    for template in list(get_database().templates.find({}))
})


class AgentSchema(BaseModel):
    id: str
    name: str
    character: str


class AgentResponse(BaseModel):
    id: str
    prompt: str
    response: str
    model: str
    timestamp: datetime


class AgentInteraction(BaseModel):
    action: AgentsActions
    agent: AgentNames
    content: Annotated[str, Field(min_length=0, max_length=255)]

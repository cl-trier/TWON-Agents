from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from ..database import get_database


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


AgentNames = Enum('AgentNames', {
    agent['id']: agent['id']
    for agent in list(get_database().agents.find({}))
})

AgentsActions = Enum('AgentActions', {
    template['id']: template['id']
    for template in list(get_database().templates.find({}))
})

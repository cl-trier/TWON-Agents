from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from ...schemas import get_explicit_agent_config, get_explicit_agent_definition
from ...services import hf_inference

"""
SETUP:
"""

SETUP: dict = {
    'config': get_explicit_agent_config(),
    'definition': get_explicit_agent_definition(),
}

router = APIRouter()

"""
TYPES:
"""

# ToDo: add example to response model
class AgentResponse(BaseModel):
    id: str
    prompt: str
    response: str
    model: str
    timestamp: str


# ToDo: Infer types from data schema
AgentTypes = Literal[
    'base', 'agreeing', 'disagreeing',
    'conspiracy_theorist', 'nobel_prize_winner', 'us_congress_member'
]

ActionTypes = Literal['read', 'like', 'share', 'reply']

"""
ROUTES:
"""


@router.get("/agents/explicit")
async def get_explicit_agents():
    return SETUP


@router.get("/agents/explicit/")
async def get_explicit_agent(
        content: str,
        character: AgentTypes = 'base',
        action: ActionTypes = 'reply'
):
    return hf_inference(
        model=SETUP["config"]["model"],
        template=SETUP["config"]["prompts"][action],
        character=SETUP["definition"][character]["persona"],
        content=content
    )

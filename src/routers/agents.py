from typing import Literal

from fastapi import APIRouter

from ..schemas import get_explicit_agent_config, get_explicit_agent_definition
from ..services import hf_post_prompt

SETUP: dict = {
    'config': get_explicit_agent_config(),
    'definition': get_explicit_agent_definition(),
}

agent_router = APIRouter()


@agent_router.get("/agents/explicit")
async def get_agents():
    return SETUP


@agent_router.get("/agents/explicit/")
async def get_agent(
        content: str,
        character: Literal[
            'base', 'agreeing', 'disagreeing',
            'conspiracy_theorist', 'nobel_prize_winner', 'us_congress_member'
        ] = 'base',
        action: Literal[
            'read', 'like', 'share', 'reply'
        ] = 'reply'
):
    request = hf_post_prompt(
        SETUP["config"]["model"],
        _fill_prompt(content, character, action)
    )
    return request.json()[0]


def _fill_prompt(content, character, action) -> str:
    return (
        SETUP["config"]["prompts"][action]
        .replace('{content}', content)
        .replace('{character}', SETUP["definition"][character]["persona"])
    )

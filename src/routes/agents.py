import datetime
import uuid
from typing import Dict

from fastapi import APIRouter

from ..inference import inference
from ..schemas import AppConfig, InteractionRequest, InteractionResponse, Persona


def create_route(config: AppConfig) -> APIRouter:
    router = APIRouter()

    @router.get(
        '/agents/',
        tags=["agents"],
        description=open(f'{config.docs_path}/agents.get.md').read()
    )
    async def get_all_personas() -> Dict[str, Persona]:
        return config.agents.personas

    @router.post(
        "/agents/",
        tags=["agents"],
        description=open(f'{config.docs_path}/agents.post.md').read()
    )
    async def generate_agent_interaction(body: InteractionRequest) -> InteractionResponse:
        merged_persona: Persona = config.agents.personas[body.personas[0]]
        for persona in body.personas[1:]:
            merged_persona = merged_persona.merge(config.agents.personas[persona])

        response: InteractionResponse = InteractionResponse(
            **inference(
                template=config.agents.prompts[body.action],
                variables=dict(
                    persona=merged_persona.persona,
                    history=body.history,
                    thread=body.thread,
                ),
                integration=body.integration,
            )
              | dict(
                id=uuid.uuid1(),
                timestamp=datetime.datetime.now(),
                action=body.action,
                persona=merged_persona,
                integration=body.integration,
            )
        )
        response.log(config.agents.log_path)

        return response

    return router

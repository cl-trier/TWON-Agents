import datetime
import uuid
from typing import Dict

from fastapi import APIRouter

from ..inference import inference
from ..schemas import AppConfig, AgentRequest, AgentResponse, Persona


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
    async def generate_agent_interaction(body: AgentRequest) -> AgentResponse:
        persona: Persona = Persona.merge_personas(body.personas, config.agents.personas)

        response: AgentResponse = AgentResponse(
            **inference(
                template=config.agents.prompts[body.action],
                variables=dict(
                    persona=str(persona),
                    history=str(body.history),
                    thread=str(body.thread),
                ),
                integration=body.integration,
            )
              | dict(
                id=uuid.uuid1(),
                timestamp=datetime.datetime.now(),
                action=body.action,
                persona=persona,
                integration=body.integration,
            )
        )
        response.log(config.agents.log_path)

        return response

    return router

from fastapi import APIRouter

from ..inference import inference
from ..schemas import Config, Response, Persona
from ..schemas.requests import GenerateRequest


def create_route(config: Config) -> APIRouter:
    router = APIRouter()

    @router.post(
        "/generate/",
        tags=["action"],
        summary='todo',
        description=open(f'{config.docs_path}/generate.md').read()
    )
    async def generate(request: GenerateRequest) -> Response:
        return Response(
            **inference(
                template=config.agents.prompts['generate'],
                persona=Persona.merge_personas(request.personas, config.agents.personas),
                request=request,
                slots=dict(topic=request.topic, length=request.length),
            ) | dict(action='generate', log_path=config.agents.log_path)
        )

    return router

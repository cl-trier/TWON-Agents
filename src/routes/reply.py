from fastapi import APIRouter

from ..inference import inference
from ..schemas import Config, Response, Persona
from ..schemas.requests import ReplyRequest


def create_route(config: Config) -> APIRouter:
    router = APIRouter()

    @router.post(
        "/reply/",
        tags=["action"],
        summary='todo',
        description=open(f'{config.docs_path}/reply.md').read()
    )
    async def reply(request: ReplyRequest) -> Response:
        return Response(
            **inference(
                template=config.agents.prompts['reply'],
                persona=Persona.merge_personas(request.personas, config.agents.personas),
                request=request,
                slots=dict(thread=request.thread, length=request.length),
            ) | dict(action='reply', log_path=config.agents.log_path)
        )

    return router

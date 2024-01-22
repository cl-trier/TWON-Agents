import re
from typing import List

from fastapi import APIRouter

from ..inference import inference
from ..schemas import Config, Response, Persona
from ..schemas.requests import LikeRequest


def create_route(config: Config) -> APIRouter:
    router = APIRouter()

    @router.post(
        "/like/",
        tags=["action"],
        summary='todo',
        description=open(f'{config.docs_path}/like.md').read()
    )
    async def like(request: LikeRequest) -> Response:
        return Response(
            **inference(
                template=config.agents.prompts['like'],
                persona=Persona.merge_personas(request.personas, config.agents.personas),
                request=request,
                slots=dict(post=request.post),
            ) | dict(action='like', log_path=config.agents.log_path)
        )

    return router

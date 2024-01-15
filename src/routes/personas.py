from typing import Dict

from fastapi import APIRouter

from ..schemas import Config, Persona


def create_route(config: Config):
    router = APIRouter()

    @router.get(
        '/personas/',
        summary='todo',
        description=open(f'{config.docs_path}/personas.md').read()
    )
    async def personas() -> Dict[str, Persona]:
        return config.agents.personas

    return router

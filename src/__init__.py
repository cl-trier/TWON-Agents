import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from .database import get_database
from .routers import create_explicit_agent_route, create_manual_distributor_route


def create_app(config: dict):
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = get_database().config.find_one({'id': 'hf_token'})['value']

    app = FastAPI(
        title=config["TITLE"],
        description=open(f'{config["DOCS"]}/Root.md').read(),
        version=config["VERSION"],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config['misc']['trust_origins'],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def redirect__to_docs():
        return RedirectResponse(url='/docs')

    for router in [
        create_explicit_agent_route(),
        create_manual_distributor_route()
    ]:
        app.include_router(router)

    return app

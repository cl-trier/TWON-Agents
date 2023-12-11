from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routes import (create_agent_route, create_docs_route)
from .schemas import AppConfig


def create_app(config: AppConfig):
    app = FastAPI(
        title=config.title,
        description=open(f'{config.docs_path}/index.md').read(),
        version=config.version,
        docs_url=None
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.trust_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in [
        create_docs_route(app),
        create_agent_route(config),
    ]:
        app.include_router(router)

    return app

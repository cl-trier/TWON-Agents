from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routes import (
    # default
    create_personas_route,
    # actions
    create_reply_route,
    create_generate_route,
    create_like_route
)
from .schemas import Config


def create_app(config: Config):
    app = FastAPI(
        title=config.title,
        description=open(f'{config.docs_path}/__index__.md').read(),
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
        create_personas_route(config),

        create_generate_route(config),
        create_reply_route(config),
        create_like_route(config),
    ]:
        app.include_router(router)

    return app

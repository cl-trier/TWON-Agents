import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routers import create_explicit_agent_route


def create_app(config: dict):
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = config['inference']['token']

    app = FastAPI(
        title=config["TITLE"],
        description=open(f'{config["DOCS"]}/Root.md').read(),
        version=config["VERSION"],
    )

    @app.get("/")
    async def redirect_docs():
        return RedirectResponse(url='/docs')

    for router in [
        create_explicit_agent_route()
    ]:
        app.include_router(router)

    return app

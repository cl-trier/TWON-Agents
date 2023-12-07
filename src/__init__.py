from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from .agents import create_route as create_agent_route
from .docs import create_route as create_docs_route
from .config import Config


def create_app(conf: Config):
    app = FastAPI(
        title=conf.title,
        description=open(f'{conf.docs_path}/Root.md').read(),
        version=conf.version,
        docs_url=None
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf.trust_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def redirect_to_docs():
        """
        The route redirects the API root to the Swagger API documentation page.
        """
        return RedirectResponse(url='/docs')

    for router in [
        create_agent_route(conf),
        create_docs_route(app)
    ]:
        app.include_router(router)

    return app

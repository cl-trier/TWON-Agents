import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pymongo import MongoClient
from starlette.middleware.cors import CORSMiddleware

from .agents import create_route as create_agent_route
from .config import Config
from .distributor import create_route as create_distributor_route


def create_app(conf: Config):
    def get_database():
        return MongoClient(host=conf.database.host, authSource='admin').twon

    os.environ["HUGGINGFACEHUB_API_TOKEN"] = get_database().config.find_one({'id': 'hf_token'})['value']

    app = FastAPI(
        title=conf.title,
        description=open(f'{conf.docs_path}/Root.md').read(),
        version=conf.version,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf.misc.trust_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def redirect__to_docs():
        """
        The route redirects the API root to the Swagger API documentation page.
        """
        return RedirectResponse(url='/docs')

    for router in [
        create_agent_route(get_database),
        create_distributor_route()
    ]:
        app.include_router(router)

    return app

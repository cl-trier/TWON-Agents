from typing import Dict

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from src.schemas import Config, Persona


config = Config.load('./app.config.toml')

app = FastAPI(
    title=config.title,
    description=open(f'./api/docs/index.md').read(),
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


@app.get("/")
async def redirect_to_docs():
    """
    The route redirects the API root to the Swagger API documentation page.
    """
    return RedirectResponse(url='/docs')


@app.get(
    '/personas/',
    summary='todo',
    description=open(f'./api/docs/personas.md').read()
)
async def personas() -> Dict[str, Persona]:
    return config.agents.personas

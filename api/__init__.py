from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src
from src.schemas import requests
from .config import Config

app = FastAPI(
    title=Config.title,
    description=open(f'{Config.docs_path}/index.md').read(),
    version=Config.version,
    docs_url='/'
)

agents = src.Agents(
    persona_src_path=Config.persona_src_path,
    prompt_src_path=Config.prompt_src_path,
    log_path=Config.log_path
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.trust_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    '/personas/',
    tags=["information"],
    summary='Retrieve all persona data',
    description=open(f'{Config.docs_path}/personas.md').read()
)
async def personas() -> Dict[str, src.Persona]:
    return agents.personas


@app.get(
    '/prompts/',
    tags=["information"],
    summary='Retrieve all prompt data',
    description=open(f'{Config.docs_path}/prompts.md').read()
)
async def prompts() -> Dict[str, str]:
    return agents.prompts


@app.post(
    "/generate/",
    tags=["action"],
    summary='todo',
    description=open(f'{Config.docs_path}/generate.md').read()
)
async def generate(request: requests.GenerateRequest) -> src.Response:
    return agents.generate(request)


@app.post(
    "/like/",
    tags=["action"],
    summary='todo',
    description=open(f'{Config.docs_path}/like.md').read()
)
async def like(request: requests.LikeRequest) -> src.Response:
    return agents.like(request)


@app.post(
    "/reply/",
    tags=["action"],
    summary='todo',
    description=open(f'{Config.docs_path}/reply.md').read()
)
async def reply(request: requests.ReplyRequest) -> src.Response:
    return agents.reply(request)

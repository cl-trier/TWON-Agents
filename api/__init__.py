import typing

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src
from src.schemas import requests
from .config import Config

from .huggingface import Huggingface, InferenceFinetunedRequest

cfg = Config()

app = FastAPI(
    title=cfg.title,
    description=open(f'{cfg.docs_path}/index.md').read(),
    version=cfg.version,
    docs_url='/'
)

agents = src.Agents(
    persona_src_path=cfg.persona_src_path,
    prompt_src_path=cfg.prompt_src_path,
    log_path=cfg.log_path
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.trust_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    '/personas/',
    tags=["information"],
    summary='Retrieve all persona data',
    description=open(f'{cfg.docs_path}/personas.md').read()
)
async def personas() -> typing.Dict[str, src.Persona]:
    return agents.personas


@app.get(
    '/prompts/',
    tags=["information"],
    summary='Retrieve all prompt data',
    description=open(f'{cfg.docs_path}/prompts.md').read()
)
async def prompts() -> typing.Dict[str, str]:
    return agents.prompts


@app.post(
    "/generate/",
    tags=["action"],
    summary='todo',
    description=open(f'{cfg.docs_path}/generate.md').read()
)
async def generate(request: requests.GenerateRequest) -> src.Response:
    return agents.generate(request)


@app.post(
    "/like/",
    tags=["action"],
    summary='todo',
    description=open(f'{cfg.docs_path}/like.md').read()
)
async def like(request: requests.LikeRequest) -> src.Response:
    return agents.like(request)


@app.post(
    "/reply/",
    tags=["action"],
    summary='todo',
    description=open(f'{cfg.docs_path}/reply.md').read()
)
async def reply(request: requests.ReplyRequest) -> src.Response:
    return agents.reply(request)


@app.post("/inference_finetuned/", tags=["hackathon"])
async def inference_finetuned(request: InferenceFinetunedRequest) -> str:
    return Huggingface(
        llm_slug=request.slug, auth_token=request.auth_token, inference_config=request.config
        ).inference(
            system=request.system_prompt,
            prompt=request.prompt
        )

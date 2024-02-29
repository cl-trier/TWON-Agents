import glob
import json
import pathlib

from dotenv import load_dotenv
from pydantic import BaseModel

from src.persona import Persona
from src.response import Response
from src.schemas import requests

load_dotenv()


class Agents(BaseModel):
    persona_src_path: str
    prompt_src_path: str

    log_path: str = None

    personas: dict[str, Persona] = {}
    prompts: dict[str, str] = {}

    def __init__(self, **data):
        super().__init__(**data)

        for persona_fl in glob.glob(f'{self.persona_src_path}/*.json'):
            _persona = Persona(**json.load(open(persona_fl)))
            self.personas[_persona.id] = _persona

        for prompt_fl in glob.glob(f'{self.prompt_src_path}/*.txt'):
            self.prompts[pathlib.Path(prompt_fl).stem] = open(prompt_fl).read()

    def __call__(self, action: str, request: requests.BaseRequest, **slots) -> Response:
        persona: Persona = Persona.merge_personas(request.personas, self.personas)
        prompt: str = self.prompts[action].format(
            persona=persona,
            language=request.language,
            platform=request.platform,
            history=request.history,
            **slots
        )

        return Response(
            action=action,
            promp=prompt,
            response=request.integration(prompt),
            persona=persona,
            integration=request.integration,
            log_path=self.log_path
        )

    def generate(self, request: requests.GenerateRequest) -> Response:
        return self('generate', request, topic=request.topic, length=request.length)

    def reply(self, request: requests.ReplyRequest) -> Response:
        return self('reply', request, thread=request.thread, length=request.length)

    def like(self, request: requests.LikeRequest) -> Response:
        return self('like', request, post=request.post)

import glob
import json
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

from src.article import Article
from src.inference import inference
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
            self.prompts[Path(prompt_fl).stem] = open(prompt_fl).read()

    def act(self, action: str, request: requests.BaseRequest, **slots) -> Response:
        return Response(**dict(
            **inference(
                template=self.prompts[action],
                persona=Persona.merge_personas(request.personas, self.personas),
                request=request,
                slots=dict(**slots),
            ) | dict(action=action, log_path=self.log_path)
        ))

    def generate(self, request: requests.GenerateRequest) -> Response:
        article = Article(topic=request.topic)
        response = self.act('generate', request, topic=str(article), length=request.length)

        response.response = f'{response.response} {article.url}'

        return response

    def reply(self, request: requests.ReplyRequest) -> Response:
        return self.act('reply', request, thread=request.thread, length=request.length)

    def like(self, request: requests.LikeRequest) -> Response:
        return self.act('like', request, post=request.post)

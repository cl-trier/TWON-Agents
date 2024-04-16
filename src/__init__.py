import glob
import json
import pathlib
import typing

import dotenv
import newspaper
import pydantic

from src.article import Article
from src.persona import Persona
from src.response import Response, ResponseMeta
from src.schemas import requests

dotenv.load_dotenv()


class Agents(pydantic.BaseModel):
    persona_src_path: str
    prompt_src_path: str

    log_path: str = None

    personas: typing.Dict[typing.Tuple[str, str], Persona] = {}
    prompts: typing.Dict[typing.Tuple[str, str], str] = {}

    def __init__(self, **data):
        super().__init__(**data)

        self.personas = {
            ((name := pathlib.Path(persona_fl).stem.split('.'))[0], name[1]): Persona(**json.load(open(persona_fl)))
            for persona_fl in glob.glob(f'{self.persona_src_path}/*.json')
        }

        self.prompts = {
            ((name := pathlib.Path(prompt_fl).stem.split('.'))[0], name[1]): open(prompt_fl).read()
            for prompt_fl in glob.glob(f'{self.prompt_src_path}/*.txt')
        }

    def __call__(self, action: str, request: requests.BaseRequest, **slots) -> Response:
        persona: Persona = Persona.merge_personas(request.language.lower(), request.persona, self.personas)
        prompt: str = self.prompts[(request.language.lower(), action)].format(
            language=request.language,
            platform=request.platform,
            history=request.history,
            **slots
        )

        return Response(
            action=action,
            prompt=prompt,
            response=request.integration(str(persona), prompt),
            persona=persona,
            integration=request.integration,
            log_path=self.log_path
        )

    def generate(self, request: requests.GenerateRequest) -> Response:
        if request.options.retrieve_google_news:
            try:
                art = Article(topic=request.topic, language=request.language, country=request.language)
                resp = self(
                    'generate',
                    request,
                    topic=str(art),
                    length=request.length,
                )
                resp.meta = ResponseMeta(retrieved_source=art.url)

                if request.options.include_news_src_link:
                    response.response = f'{resp.response}\n\n{art.url}'

            except (
                    newspaper.article.ArticleException,
                    requests.exceptions.ConnectionError
            ):
                resp = self('generate', request, topic=request.topic, length=request.length)

        else:
            resp = self('generate', request, topic=request.topic, length=request.length)

        return resp

    def reply(self, request: requests.ReplyRequest) -> Response:
        return self('reply', request, thread=request.thread, length=request.length)

    def like(self, request: requests.LikeRequest) -> Response:
        return self('like', request, post=request.post)

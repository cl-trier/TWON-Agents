import glob
import json
from pathlib import Path

from pydantic import BaseModel

from .inference import inference
from .persona import Persona
from .schemas.requests import BaseRequest, GenerateRequest, ReplyRequest, LikeRequest


class Agents(BaseModel):
    persona_src_path: str
    prompt_src_path: str

    personas: dict[str, Persona] = {}
    prompts: dict[str, str] = {}

    def __init__(self, **data):
        super().__init__(**data)

        for persona_fl in glob.glob(f'{self.persona_src_path}/*.json'):
            _persona = Persona(**json.load(open(persona_fl)))
            self.personas[_persona.id] = _persona

        for prompt_fl in glob.glob(f'{self.prompt_src_path}/*.txt'):
            self.prompts[Path(prompt_fl).stem] = open(prompt_fl).read()

    def act(self, action: str, request: BaseRequest, **slots):
        return dict(
            **inference(
                template=self.prompts[action],
                persona=Persona.merge_personas(request.personas, self.personas),
                request=request,
                slots=dict(**slots),
            ) | dict(action=action)
        )

    def generate(self, request: GenerateRequest, **slots):
        return self.act('generate', request, **slots)

    def reply(self, request: ReplyRequest, **slots):
        return self.act('reply', request, **slots)

    def like(self, request: LikeRequest, **slots):
        return self.act('like', request, **slots)

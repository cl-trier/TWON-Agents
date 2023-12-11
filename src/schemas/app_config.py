import glob
import json
import tomllib
from pathlib import Path
from typing import List

from pydantic import BaseModel

from .persona import Persona


class AgentsConfig(BaseModel):
    persona_src_path: str
    prompt_src_path: str
    log_path: str

    personas: dict[str, Persona] = {}
    prompts: dict[str, str] = {}

    def __init__(self, **data):
        super().__init__(**data)

        Path(self.log_path).mkdir(parents=True, exist_ok=True)

        for persona_fl in glob.glob(f'{self.persona_src_path}/*.json'):
            persona = Persona(**json.load(open(persona_fl)))
            self.personas[persona.id] = persona

        for prompt_fl in glob.glob(f'{self.prompt_src_path}/*.txt'):
            self.prompts[Path(prompt_fl).stem] = open(prompt_fl).read()


class AppConfig(BaseModel):
    title: str
    version: str
    docs_path: str

    trust_origins: List[str]

    agents: AgentsConfig

    @classmethod
    def load(cls, path: str) -> 'AppConfig':
        return cls(**tomllib.load(open(path, "rb")))

import tomllib
from typing import List

from pydantic import BaseModel


class LoggingConfig(BaseModel):
    agent_path: str


class Config(BaseModel):
    title: str
    version: str
    docs_path: str

    trust_origins: List[str]

    logging: LoggingConfig

    @classmethod
    def load(cls, path):
        return cls(**tomllib.load(open(path, "rb")))

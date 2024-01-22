
import tomllib
from typing import List

from pydantic import BaseModel


class Config(BaseModel):
    title: str
    version: str
    docs_path: str

    trust_origins: List[str]


    @classmethod
    def load(cls, path: str) -> 'Config':
        return cls(**tomllib.load(open(path, "rb")))

import tomllib
from typing import List

from pydantic import BaseModel


class MiscConfig(BaseModel):
    trust_origins: List[str]


class DatabaseConfig(BaseModel):
    host: str


class Config(BaseModel):
    title: str
    version: str
    docs_path: str

    database: DatabaseConfig
    misc: MiscConfig

    @classmethod
    def load(cls, path):
        return cls(**tomllib.load(open(path, "rb")))

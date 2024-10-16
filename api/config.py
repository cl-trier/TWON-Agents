import pathlib
import typing


class Config:
    title: str = 'TWON Agents API'
    version: str = '0.0.3'

    trust_origins: typing.List[str] = ['*']

    persona_src_path: str = './data/personas'
    prompt_src_path: str = './data/prompts'

    docs_path: str = './api/docs'
    log_path: str = './api/logs'

    def __init__(self) -> None:
        self.log_path = f'{self.log_path}/{self.version}'
        pathlib.Path(self.log_path).mkdir(parents=True, exist_ok=True)

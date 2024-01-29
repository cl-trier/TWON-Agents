from pathlib import Path
from typing import List


class Config:
    title: str = 'TWON Agents API'
    version: str = '0.0.1'

    trust_origins: List[str] = [
        'http://localhost:5173',
        'http://localhost:8000',
    ]

    persona_src_path: str = './data/personas'
    prompt_src_path: str = './data/prompts'

    docs_path: str = './api/docs'
    log_path: str = './api/logs'

    def __init__(self) -> None:
        self.log_path = f'{self.log_path}/{self.version}'
        Path(self.log_path).mkdir(parents=True, exist_ok=True)

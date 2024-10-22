import typing

import ollama
import openai
import pydantic


class Integration(pydantic.BaseModel):
    provider: typing.Literal['local', 'OpenAI']
    model: typing.Literal[
        'falcon:40b-instruct-q5_1',
        'gemma:7b-instruct-q6_K',
        'llama2:70b-chat-q6_K',
        'mistral:7b-instruct-v0.2-q6_K',
        'mixtral:8x7b-instruct-v0.1-q6_K',
        'qwen:72b-chat-v1.5-q6_K',
        "llama3.1:70b-instruct-q6_K",
        'gpt-3.5-turbo', 'gpt-4',
    ]

    def __call__(self, system: str, prompt: str) -> str:
        messages: typing.List[typing.Dict] = [
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        return self.endpoints[self.provider](self.model, messages)

    @property
    def endpoints(self) -> typing.Dict[str, callable]:
        return {
            'local': lambda model, messages: (
                ollama
                .chat(
                    model=model,
                    messages=messages
                )
                ['message']
                ['content']
            ),
            'OpenAI': lambda model, messages: (
                openai.OpenAI()
                .chat
                .completions
                .create(
                    model=model,
                    messages=messages
                )
                .choices[0]
                .message
                .content
            )
        }

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "provider": "local",
                    "model": "mixtral:8x7b-instruct-v0.1-q6_K",
                },
                {
                    "provider": "OpenAI",
                    "model": "gpt-4",
                },
            ]
        }
    }

import random
import sys
import typing

import huggingface_hub
import ollama
import openai
import pydantic


class Integration(pydantic.BaseModel):
    provider: typing.Literal['local', 'huggingFace', 'OpenAI']
    model: typing.Literal[
        'llama2:7b', 'llama2:14b', 'llama2:70b',
        'qwen:7b', 'qwen:14b', 'qwen:72b',
        'mistral:v0.2', 'mixtral:8x7b',
        'falcon:7b', 'falcon:40b',
        'gemma:7b',

        'gpt-3.5-turbo', 'gpt-4',

        'mistralai/Mistral-7B-Instruct-v0.2', 'google/gemma-7b'
    ]

    def __call__(self, prompt: str) -> str:
        return self.endpoints[self.provider](prompt, self.model)

    @property
    def endpoints(self) -> typing.Dict[str, callable]:
        return {
            'local': lambda prompt, model: (
                ollama
                .chat(
                    model=model,
                    messages=[
                        {
                            'role': 'user',
                            'content': prompt,
                        },
                    ]
                )
                ['message']
                ['content']
            ),
            'huggingFace': lambda prompt, model: (
                huggingface_hub.InferenceClient(model)
                .text_generation(
                    prompt,
                    max_new_tokens=255,
                    seed=random.randint(0, sys.maxsize)
                )
            ),
            'OpenAI': lambda prompt, model: (
                openai.OpenAI()
                .chat
                .completions
                .create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model=model
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
                    "model": "llama2:70b",
                },
                {
                    "provider": "huggingFace",
                    "model": "mistralai/Mistral-7B-Instruct-v0.2",
                },
                {
                    "provider": "OpenAI",
                    "model": "gpt-4",
                },
            ]
        }
    }

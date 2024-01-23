import random
import sys

from huggingface_hub import InferenceClient
from openai import OpenAI

from src.persona import Persona
from src.schemas.requests import BaseRequest


def inference(
        template: str,
        slots: dict,
        persona: Persona,
        request: BaseRequest
) -> dict:
    prompt: str = template.format(
        **dict(
            language=str(request.language),
            platform=str(request.platform),
            history=str(request.history),
            persona=str(persona)
        ) | slots
    )

    return {
        'prompt': prompt,
        'integration': request.integration,
        'persona': persona,
        'response': {
            'huggingFace': hf_inference,
            'OpenAI': oai_inference,
        }[request.integration.provider](
            prompt,
            model=request.integration.model
        ).strip('\n').strip(),
    }


def hf_inference(prompt: str, model: str) -> str:
    return (
        InferenceClient(model)
        .text_generation(
            prompt,
            max_new_tokens=255,
            seed=random.randint(0, sys.maxsize)
        )
    )


def oai_inference(prompt: str, model: str) -> str:
    return (
        OpenAI()
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

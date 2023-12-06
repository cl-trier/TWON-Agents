from huggingface_hub import InferenceClient
from openai import OpenAI

from .schemas import EndpointSchema


def inference(
        template: str,
        variables: dict,
        endpoint: EndpointSchema
) -> dict:
    prompt: str = template.format(**variables)

    return {
        'prompt': prompt,
        'response': {
            'huggingFace': hf_inference,
            'OpenAI': oai_inference,
        }[endpoint.integration](
            prompt,
            model=endpoint.model
        ).strip('\n').strip(),
    }


def hf_inference(prompt: str, model: str) -> str:
    return (
        InferenceClient(model)
        .text_generation(
            prompt,
            max_new_tokens=250
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

import uuid
import datetime

from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate


def hf_inference(
        model: str,
        template: str,
        model_args=dict,
        **kwargs
) -> dict:
    prompt: str = PromptTemplate(
        template=template,
        input_variables=list(kwargs.keys())
    ).format(**kwargs)

    response: str = HuggingFaceHub(
        repo_id=model,
        model_kwargs=model_args
    )(prompt)

    return {
        'id': f'hf-{uuid.uuid1()}',
        'prompt': prompt,
        'response': response,
        'model': model,
        'timestamp': datetime.datetime.now(),
    }

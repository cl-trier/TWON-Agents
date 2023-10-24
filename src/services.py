import uuid
import datetime

from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

MODEL_CONFIG: dict = {
    "temperature": 0.5,
    "max_length": 244
}


# ToDo: log all requests/responses to database
def hf_inference(model: str, template: str, **kwargs):
    prompt: str = PromptTemplate(
        template=template,
        input_variables=list(kwargs.keys())
    ).format(**kwargs)

    response: str = HuggingFaceHub(
        repo_id=model,
        model_kwargs=MODEL_CONFIG
    )(prompt)

    return [{
        'id': f'hf-{uuid.uuid1()}',
        'prompt': prompt,
        'response': response,
        'model': model,
        'timestamp': datetime.datetime.now(),
    }]

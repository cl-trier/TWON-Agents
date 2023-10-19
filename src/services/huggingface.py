import requests

ENDPOINT: str = 'https://api-inference.huggingface.co/models'
BEARER: str = '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'


def hf_post_prompt(model: str, prompt: str) -> requests.Response:
    return requests.post(
        f'{ENDPOINT}/{model}',
        json={
            "inputs": prompt,
            "parameters": {
                "return_full_text": False,
                "max_new_tokens": 200,
            }

        },
        headers={
            "Authorization": f'Bearer {BEARER}'
        }
    )

import typing

import pydantic

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from twon_agents.align_action_likelihood.model import Model


class Request(pydantic.BaseModel):
    batch_history: typing.List[typing.List[str]]
    batch_post: typing.List[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "batch_history": [
                        ["History 1.a", "History 1.b"], 
                        ["History 2.a", "History 2.b"]
                    ],
                    "batch_post": ["Post 1", "Post 2"]
                }
            ]
        }
    }


class Response(pydantic.BaseModel):
    predictions: typing.List[float]


app = FastAPI(
    title="TWON - Agent Action Likelihood",
    version="0.0.1",
    docs_url="/"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

model, _ = Model.load("models/decision/en/model.pth")

@app.post("/v1/inference/")
async def inference(request: Request) -> Response:
    return Response(predictions=model.predict(**request.model_dump()))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
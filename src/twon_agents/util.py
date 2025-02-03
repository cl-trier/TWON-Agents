import typing

import pandas
from rich.progress import track

import transformers


def load_pipelines(
    models: typing.Dict[str, str], disable_sampling: bool = True
) -> typing.Dict[str, transformers.Pipeline]:
    pipelines: typing.Dict[str, transformers.Pipeline] = {
        label: transformers.pipeline("text-generation", slug)
        for _, (label, slug) in enumerate(models.items())
    }

    for label in pipelines.keys():
        pipelines[label].model.generation_config.pad_token_id = pipelines[
            label
        ].tokenizer.pad_token_id

        if disable_sampling:
            pipelines[label].model.generation_config.do_sample = False

    if "adapter" in pipelines.keys():
        pipelines["adapter"].model.load_adapter(models["adapter"])

    return pipelines


def generated_w_pipelines(
    pipelines: typing.Dict[str, transformers.Pipeline],
    dataset: typing.List[typing.Dict],
) -> pandas.DataFrame:
    responses = []

    for idx, chat in enumerate(track(dataset)):
        responses.append(
            dict(id=idx, model="human", text=chat["messages"][-1]["content"])
        )

        for model, pipeline in pipelines.items():
            reply = pipeline(
                pipeline.tokenizer.apply_chat_template(
                    chat["messages"][:-1], tokenize=False
                ),
                max_new_tokens=128,
                return_full_text=False,
                pad_token_id=pipeline.tokenizer.eos_token_id,
            )[0]["generated_text"].split("\n\n")[1]

            responses.append(dict(id=idx, model=model, text=reply))

    return pandas.DataFrame(responses).set_index("id").pivot(columns=["model"])

import typing 

import transformers


def load_pipelines(models: typing.Dict[str, str]) -> typing.Dict[str, transformers.Pipeline]:
    pipelines: typing.Dict[str, transformers.Pipeline] = {
        label: transformers.pipeline("text-generation", slug)
        for n, (label, slug) in enumerate(models.items())
    }

    if "adapter" in pipelines.keys():
        pipelines["adapter"].model.load_adapter(models["adapter"])

    return pipelines
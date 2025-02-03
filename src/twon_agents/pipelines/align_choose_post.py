import pydantic

import transformers

import pytorch


class DecisionModel(pytorch.nn.Module):
    def __init__(self, input_size: int, output_size: int):
        super().__init__()

        self.history_representation: pytorch.nn.Module = None
        self.feed_representation: pytorch.nn.Module = None


class AlignChoosePost(pydantic.BaseModel):
    embed_model: str = "Twitter/twhin-bert-base"

    def __call__(self):
        tokenizer = transformers.AutoTokenizer.from_pretrained(self.embed_model)
        model = transformers.AutoModel.from_pretrained(self.embed_model)

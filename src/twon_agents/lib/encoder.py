import typing

import transformers
import torch


class Encoder:
    # information on the model: https://arxiv.org/abs/2209.07562
    def __init__(self, model: str = "Twitter/twhin-bert-base"):
        self.model = dict(
            tokenizer=transformers.AutoTokenizer.from_pretrained(model),
            transformer=transformers.AutoModel.from_pretrained(model).to("cuda"),
        )

    def __call__(self, batch: typing.List[str]):
        return self._pool(
            self.model["transformer"](
                **self.model["tokenizer"](
                    batch,
                    padding=True,
                    return_tensors="pt",
                ).to("cuda")
            ).last_hidden_state
        )

    @staticmethod
    def _pool(batch: torch.Tensor, method: typing.Literal["mean", "cls"] = "mean"):
        return dict(mean=lambda x: x.mean(dim=1), cls=lambda x: x[:, 0, :])[method](
            batch
        )

    @property
    def num_dim(self) -> int:
        return self.model["transformer"].config.to_dict()["hidden_size"]

import typing

import pydantic

import torch

from twon_agents.lib import Encoder, functional


class ModelArgs(pydantic.BaseModel):
    encoder_model: str = "Twitter/twhin-bert-base"
    history_length: int = 2
    dropout_ratio: float = 0.1


class Model(torch.nn.Module):
    @functional.timeit
    def __init__(self, args: ModelArgs):
        super().__init__()

        self.args = args
        self.encoder = Encoder(self.args.encoder_model)

        self.history_representation: torch.nn.Linear = torch.nn.Linear(
            self.encoder.num_dim * self.args.history_length,
            self.encoder.num_dim * self.args.history_length,
        )
        self.post_representation: torch.nn.Linear = torch.nn.Linear(
            self.encoder.num_dim, self.encoder.num_dim
        )

        self.dimension_reduction: torch.nn.Linear = torch.nn.Linear(
            self.encoder.num_dim * self.args.history_length, 1
        )

        self.dropout: torch.nn.Dropout = torch.nn.Dropout(self.args.dropout_ratio)
        self.activiation_fn: torch.nn.Sigmoid = torch.nn.Sigmoid()

        self.to("cuda")

    def __call__(self, batch_history: torch.Tensor, batch_post: torch.Tensor):
        encoded_history = self.history_representation(batch_history)
        encoded_post = self.post_representation(batch_post).repeat(
            1, self.args.history_length
        )

        encoded_history = self.dropout(self.activiation_fn(encoded_history))
        encoded_post = self.dropout(self.activiation_fn(encoded_post))

        merged_representation: torch.Tensor = self.dimension_reduction(
            encoded_history * encoded_post
        )
        merged_representation = self.activiation_fn(merged_representation)

        return merged_representation

    def forward(self, encoded_history: torch.Tensor, encoded_post: torch.Tensor):
        return self(encoded_history.unsqueeze(0), encoded_post.unsqueeze(0))

    @torch.no_grad()
    def predict(
        self, history_batch: typing.List[typing.List[str]], post_batch: typing.List[str]
    ) -> typing.List[float]:
        encoded_history: torch.Tensor = torch.cat(
            [
                self.encoder(list(zip(*history_batch))[n])
                for n in range(self.args.history_length)
            ],
            dim=1,
        )
        encoded_post: torch.Tensor = self.encoder(post_batch)

        return self(encoded_history, encoded_post).squeeze().tolist()

    def save(self, path: str, meta: typing.Dict | None = None):
        torch.save(
            {
                "state_dict": self.state_dict(),
                "args": self.args,
                "meta": meta,
            },
            path,
        )

    @classmethod
    def load(cls: "Model", path: str) -> "Model":
        checkpoint = torch.load(path, weights_only=True)

        model: torch.nn.Module = cls(checkpoint["args"])
        model.load_state_dict(checkpoint["state_dict"])

        return model, checkpoint["meta"]


if __name__ == "__main__":
    # ---- Test: Load/Save Model ----
    test_model: Model = Model("Twitter/twhin-bert-base")
    test_model.save("models/decision/debug_model.pth")

    test_loaded_model: Model = Model.load("models/decision/debug_model.pth")

    # ---- Test: Predict Model ----
    print(
        test_model.predict(
            [["History 1.a", "History 1.b"], ["History 2.a", "History 2.b"]],
            ["Post 1", "Post 2"],
        )
    )

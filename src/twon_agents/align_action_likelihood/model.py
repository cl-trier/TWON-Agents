import typing

import torch

from twon_agents.lib import Encoder, functional


class Model(torch.nn.Module):
    @functional.timeit
    def __init__(self, encoder_model: str, history_length: int = 2):
        super(Model, self).__init__()

        self.encoder_model = encoder_model
        self.history_length = history_length

        self.encoder = Encoder(encoder_model)

        self.history_representation: torch.nn.Linear = torch.nn.Linear(
            self.encoder.num_dim * history_length, self.encoder.num_dim * history_length
        )
        self.post_representation: torch.nn.Linear = torch.nn.Linear(
            self.encoder.num_dim, self.encoder.num_dim
        )

        self.dimension_reduction: torch.nn.Linear = torch.nn.Linear(
            self.encoder.num_dim * history_length, 1
        )

        self.activiation_fn: torch.nn.Sigmoid = torch.nn.Sigmoid()

        self.to("cuda")

    def __call__(self, batch_history: torch.Tensor, batch_post: torch.Tensor):
        encoded_history = self.history_representation(batch_history)
        encoded_post = self.post_representation(batch_post).repeat(
            1, self.history_length
        )

        encoded_history = self.activiation_fn(encoded_history)
        encoded_post = self.activiation_fn(encoded_post)

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
                for n in range(self.history_length)
            ],
            dim=1,
        )
        encoded_post: torch.Tensor = self.encoder(post_batch)

        return self(encoded_history, encoded_post).squeeze().tolist()

    def save(self, path: str, meta: typing.Dict = {}):
        torch.save(
            {
                "model_state_dict": self.state_dict(),
                "encoder_model": self.encoder_model,
                "history_length": self.history_length,
                "meta": meta,
            },
            path,
        )

    @classmethod
    def load(CLS: "Model", path: str) -> "Model":
        checkpoint = torch.load(path, weights_only=True)

        model: torch.nn.Module = CLS(
            checkpoint["encoder_model"], checkpoint["history_length"]
        )
        model.load_state_dict(checkpoint["model_state_dict"])

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

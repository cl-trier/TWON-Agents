import typing

import torch

from twon_agents.lib import Encoder


class Model(torch.nn.Module):
    def __init__(self, encoder_model: str, history_length: int = 2):
        super().__init__()

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

        self.activiation_fn: torch.nn.ReLU = torch.nn.ReLU()

        self.to("cuda")

    def __call__(
        self, batch_history: typing.List[typing.List[str]], batch_post: typing.List[str]
    ):
        return torch.concat(
            [
                self.forward(history, post)
                for history, post in zip(batch_history, batch_post)
            ]
        )

    def forward(self, history: typing.List[str], post: str):
        with torch.no_grad():
            encoded_history: torch.Tensor = self.encoder(history).view(-1)
            encoded_post: torch.Tensor = self.encoder(post).view(-1)

        encoded_history = torch.autograd.Variable(
            encoded_history.data, requires_grad=True
        ).to("cuda")
        encoded_post = torch.autograd.Variable(
            encoded_post.data, requires_grad=True
        ).to("cuda")

        encoded_history = self.history_representation(encoded_history)

        encoded_post = self.post_representation(encoded_post).repeat(
            self.history_length
        )

        encoded_history = self.activiation_fn(encoded_history)
        encoded_post = self.activiation_fn(encoded_post)

        merged_representation: torch.Tensor = self.dimension_reduction(
            encoded_history * encoded_post
        )
        merged_representation = self.activiation_fn(merged_representation)

        return merged_representation

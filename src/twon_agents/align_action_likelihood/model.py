import typing

import torch

from twon_agents.lib import Encoder


class Model(torch.nn.Module):
    def __init__(self, encoder_model: str, history_length: int = 2):
        super(Model, self).__init__()

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
        return self(encoded_history.unsqueeze(), encoded_post.unsqueeze())

    def predict(self, history: typing.List[str], post: str):
        with torch.no_grad():
            encoded_history: torch.Tensor = self.encoder(history).view(-1)
            encoded_post: torch.Tensor = self.encoder(post).view(-1)

        encoded_history = torch.autograd.Variable(
            encoded_history.data, requires_grad=True
        ).to("cuda")
        encoded_post = torch.autograd.Variable(
            encoded_post.data, requires_grad=True
        ).to("cuda")

        return self.forward(encoded_history, encoded_post)

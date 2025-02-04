import typing

import pydantic

import pandas
import transformers
import torch


class DecisionModel(torch.nn.Module):
    def __init__(self, encoder_model: str, history_length: int = 2):
        super().__init__()

        self.history_length = history_length

        self.encoder = dict(
            tokenizer=transformers.AutoTokenizer.from_pretrained(encoder_model),
            model=transformers.AutoModel.from_pretrained(encoder_model),
        )

        self.history_representation: torch.nn.Linear = torch.nn.Linear(
            self.encoder_dim * history_length, self.encoder_dim * history_length
        )
        self.post_representation: torch.nn.Linear = torch.nn.Linear(
            self.encoder_dim, self.encoder_dim
        )

        self.dimension_reduction: torch.nn.Linear = torch.nn.Linear(
            self.encoder_dim * history_length, 1
        )

        self.activiation_fn: torch.nn.ReLU = torch.nn.ReLU()

    def forward(self, history: typing.List[str], post: str):
        with torch.no_grad():
            encoded_history: torch.Tensor = self.encode(history).view(-1)
            encoded_post: torch.Tensor = self.encode(post).view(-1)

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

    def encode(self, batch: typing.List[str]):
        return self.encoder["model"](
            **self.encoder["tokenizer"](
                batch,
                padding=True,
                return_tensors="pt",
            )
        ).pooler_output

    @property
    def encoder_dim(self) -> int:
        return self.encoder["model"].config.to_dict()["hidden_size"]


class Dataset(torch.utils.data.Dataset):
    def __init__(self, df: pandas.DataFrame):
        self.df = df

    def __len__(self):
        return len(self.df)

    def __getitem__(
        self, idx: typing.Union[typing.Dict, slice]
    ) -> typing.Union[typing.Dict, list[typing.Dict]]:
        return self.df.iloc[idx].to_dict()


class AlignChoosePost(pydantic.BaseModel):
    class Optimizer(pydantic.BaseModel):
        lr: float = 0.001
        betas: typing.Tuple[float, float] = (0.9, 0.999)
        eps: float = 1e-08
        weight_decay: float = 0.01

    class Training(pydantic.BaseModel):
        epochs: int = 10
        batch_size: int = 32

    encoder_model: str = "Twitter/twhin-bert-base"
    optimizer: Optimizer = Optimizer()
    training: Training = Training()

    _out_dir: str = "./models/decision"

    def model_post_init(self, __context: typing.Any) -> None:
        self.writer: torch.utils.tensorboard.SummaryWriter = (
            torch.utils.tensorboard.SummaryWriter(self._out_dir)
        )

        self.model: DecisionModel = DecisionModel(self.encoder_model)
        self.optmizer: torch.optim.AdamW = torch.optim.AdamW(
            self.model.parameters(),
        )
        self.loss_fn: torch.nn.L1Loss = torch.nn.L1Loss()

    def __call__(self):
        train_data = torch.utils.data.DataLoader(
            Dataset(), batch_size=4, shuffle=True
        )
        eval_data = torch.utils.data.DataLoader(
            Dataset(), batch_size=4, shuffle=True
        )

        for epoch in range(1, self.training.epochs + 1):
            self.model.train(True)

            self.do_epoch(train_data, epoch, "train")

            self.model.eval()
            with torch.no_grad():
                self.do_epoch(eval_data, epoch, "eval")

            self.writer.flush()

    def do_epoch(
        self,
        dataloader: torch.utils.data.DataLoader,
        epoch_index: int = 0,
        epoch_type: typing.Literal["train", "eval"] = "train",
    ):
        epoch_loss: float = 0.0

        for i, data in enumerate(dataloader):
            inputs, labels = data

            self.optimizer.zero_grad()

            outputs = self.model(inputs)

            loss: torch.Tensor = self.loss_fn(outputs, labels)
            loss.backward()

            self.optimizer.step()

            epoch_loss += loss.item()

        self.writer.add_scalar(f"loss/{epoch_type}", epoch_loss, epoch_index)


if __name__ == "__main__":
    myModel = DecisionModel("Twitter/twhin-bert-base")
    print(myModel.encoder_dim)

    print(myModel.forward(history=["History 1", "History 2"], post="Feed 1"))

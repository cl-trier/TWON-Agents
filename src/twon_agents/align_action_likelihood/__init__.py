import typing
import shutil

import pydantic

import pandas
import torch

from torch.utils.tensorboard import SummaryWriter
from rich.progress import track

from twon_agents.align_action_likelihood.dataset import Dataset
from twon_agents.align_action_likelihood.model import Model


class Pipeline(pydantic.BaseModel):
    class Dataset(pydantic.BaseModel):
        train_set: pandas.DataFrame
        test_set: pandas.DataFrame

        model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    class OptimizerArgs(pydantic.BaseModel):
        lr: float = 0.001
        betas: typing.Tuple[float, float] = (0.9, 0.999)
        eps: float = 1e-08
        weight_decay: float = 0.01

    class TrainingArgs(pydantic.BaseModel):
        epochs: int = 20
        batch_size: int = 4

    dataset: Dataset

    encoder_model: str = "Twitter/twhin-bert-base"

    optimizer_args: OptimizerArgs = OptimizerArgs()
    training_args: TrainingArgs = TrainingArgs()

    _out_dir: str = "./models/decision"

    model_config = pydantic.ConfigDict(extra="allow")

    def model_post_init(self, __context: typing.Any) -> None:
        self.writer: SummaryWriter = SummaryWriter()

        self.model: Model = Model(self.encoder_model)
        self.optimizer: torch.optim.AdamW = torch.optim.AdamW(
            self.model.parameters(),
        )
        self.loss_fn: torch.nn.L1Loss = torch.nn.L1Loss()

    def __call__(self):
        train_data = torch.utils.data.DataLoader(
            Dataset(self.dataset.train_set),
            batch_size=self.training_args.batch_size,
            shuffle=True,
            collate_fn=self._collate,
        )
        eval_data = torch.utils.data.DataLoader(
            Dataset(self.dataset.train_set),
            batch_size=self.training_args.batch_size,
            shuffle=True,
            collate_fn=self._collate,
        )

        for epoch in track(range(1, self.training_args.epochs + 1)):
            self.model.train(True)

            self.do_epoch(train_data, epoch, "train")

            self.model.eval()
            with torch.no_grad():
                self.do_epoch(eval_data, epoch, "eval")

            self.writer.flush()

        shutil.copytree("./runs/", self._out_dir, dirs_exist_ok=True)
        shutil.rmtree("./runs/")

    def do_epoch(
        self,
        dataloader: torch.utils.data.DataLoader,
        epoch_index: int = 0,
        epoch_type: typing.Literal["train", "eval"] = "train",
    ):
        epoch_loss: float = 0.0

        for i, data in enumerate(dataloader):
            history, stimulus, action = data

            self.optimizer.zero_grad()

            outputs = self.model(history, stimulus)

            loss: torch.Tensor = self.loss_fn(outputs, action)

            if epoch_type == "train":
                loss.backward()
                self.optimizer.step()

            epoch_loss += loss.item()

        self.writer.add_scalar(f"loss/{epoch_type}", epoch_loss, epoch_index)

    @staticmethod
    def _collate(batch: typing.List[typing.Dict]):
        batch_df: pandas.DataFrame = pandas.DataFrame(batch)

        return (
            batch_df[["history_1", "history_2"]].values.tolist(),
            batch_df["stimulus"].tolist(),
            torch.Tensor(batch_df["action"].astype(int).tolist()).to("cuda"),
        )


__all__ = ["Dataaset", "Model", "Pipeline"]

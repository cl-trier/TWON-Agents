import typing
import shutil
import logging

import pydantic

import pandas
import torch

from sklearn.metrics import classification_report
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
        epochs: int = 100
        batch_size: int = 32

    # ---- Main Configuration ----

    dataset: Dataset

    encoder_model: str = "Twitter/twhin-bert-base"

    optimizer_args: OptimizerArgs = OptimizerArgs()
    training_args: TrainingArgs = TrainingArgs()

    # ---- Internal Configuration ----

    _out_dir: str = "./models/decision"

    model_config = pydantic.ConfigDict(extra="allow")

    def model_post_init(self, __context: typing.Any) -> None:
        self.writer: SummaryWriter = SummaryWriter()

        self.model: Model = Model(self.encoder_model)
        self.optimizer: torch.optim.AdamW = torch.optim.AdamW(
            self.model.parameters(), **self.optimizer_args.model_dump()
        )
        self.loss_fn: torch.nn.BCELoss = torch.nn.BCELoss()

    def __call__(self):
        # ========================================
        # Data Preparation
        # ========================================
        train_data = torch.utils.data.DataLoader(
            Dataset(self.dataset.train_set, encoder=self.model.encoder),
            **self._dataloader_kwargs,
        )
        eval_data = torch.utils.data.DataLoader(
            Dataset(self.dataset.test_set, encoder=self.model.encoder),
            **self._dataloader_kwargs,
        )

        # ========================================
        # Training and Evaluation
        # ========================================
        for epoch in range(1, self.training_args.epochs + 1):
            self.model.train(True)
            with torch.enable_grad():
                self.do_epoch(train_data, epoch, "train")

            self.model.eval()
            with torch.no_grad():
                self.do_epoch(eval_data, epoch, "eval")

            self.writer.flush()

        # ========================================
        # Cleanup
        # ========================================
        shutil.copytree("./runs/", self._out_dir, dirs_exist_ok=True)
        shutil.rmtree("./runs/")

    def do_epoch(
        self,
        dataloader: torch.utils.data.DataLoader,
        epoch_index: int = 0,
        epoch_type: typing.Literal["train", "eval"] = "train",
    ):
        epoch_loss: float = 0.0
        preds: typing.Dict[str, typing.List] = dict(true=[], pred=[])

        for _, data in enumerate(track(dataloader, transient=True)):
            history, stimulus, action = data

            outputs: torch.Tensor = self.model(history, stimulus)
            loss: torch.Tensor = self.loss_fn(outputs, action.view(-1, 1))

            preds["true"].extend(action.tolist())
            preds["pred"].extend(outputs.view(-1).round(decimals=0).tolist())

            if epoch_type == "train":
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            epoch_loss += loss.item()

        evaluation = classification_report(preds["true"], preds["pred"], output_dict=True)

        logging.info((
            f"[{epoch_index:4d}] |"
            f"loss/{epoch_type}={(epoch_loss / len(dataloader)):2.4f}",
            f"f1-score/{epoch_type}={evaluation['weighted avg']['f1-score']:2.4f}"
        ))
        self.writer.add_scalars(epoch_type, dict(
                loss=epoch_loss / len(dataloader),
                f1_score=evaluation['weighted avg']['f1-score']
            ),
            global_step=epoch_index
        )

    # ========================================
    # Utility Methods
    # ========================================

    @staticmethod
    def _collate(batch: typing.List[typing.Dict]):
        batch_df: pandas.DataFrame = pandas.DataFrame(batch)

        return (
            torch.concat(
                [
                    torch.stack(batch_df["history_1"].tolist()),
                    torch.stack(batch_df["history_2"].tolist()),
                ],
                dim=1,
            ).to("cuda"),
            torch.stack(batch_df["stimulus"].tolist()).to("cuda"),
            torch.Tensor(batch_df["action"].astype(int).tolist()).to("cuda"),
        )

    @pydantic.computed_field
    @property
    def _dataloader_kwargs(self) -> typing.Dict:
        return dict(
            batch_size=self.training_args.batch_size,
            shuffle=True,
            collate_fn=self._collate,
        )


__all__ = ["Dataset", "Model", "Pipeline"]

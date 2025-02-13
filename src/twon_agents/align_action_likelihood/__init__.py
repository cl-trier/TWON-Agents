import typing
import datetime
import logging

import pydantic

import pandas
import torch

from sklearn.metrics import classification_report
from torch.utils.tensorboard import SummaryWriter
from rich.progress import track

from twon_agents.align_action_likelihood.dataset import Dataset
from twon_agents.align_action_likelihood.model import Model, ModelArgs

from twon_agents.lib import functional


class Pipeline(pydantic.BaseModel):
    class Dataset(pydantic.BaseModel):
        train_set: pandas.DataFrame
        test_set: pandas.DataFrame

        model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    class TrainingArgs(pydantic.BaseModel):
        epochs: int = 100
        batch_size: int = 256

        learning_rate: float = 0.002

    # ---- Main Configuration ----

    dataset: Dataset
    model_args: ModelArgs = ModelArgs()
    training_args: TrainingArgs = TrainingArgs()

    # ---- Internal Configuration ----

    _out_dir: str = "./models/decision"

    model_config = pydantic.ConfigDict(extra="allow")

    def model_post_init(self, __context: typing.Any) -> None:
        self.writer: SummaryWriter = SummaryWriter(
            log_dir=f"{self._out_dir}/{datetime.datetime.now()}"
        )

        self.model: Model = Model(self.model_args)
        self.optimizer: torch.optim.AdamW = torch.optim.AdamW(
            self.model.parameters(), lr=self.training_args.learning_rate
        )
        self.loss_fn: torch.nn.BCELoss = torch.nn.BCELoss()

    @functional.timeit
    def __call__(self):
        best_epoch_meta = {"epoch": -1, "metric_score": -1, "metrics": ({}, {})}

        # ========================================
        # Data Preparation
        # ========================================
        train_data = torch.utils.data.DataLoader(
            Dataset(self.dataset.train_set, encoder=self.model.encoder),
            **self._dataloader_kwargs,
        )
        test_data = torch.utils.data.DataLoader(
            Dataset(self.dataset.test_set, encoder=self.model.encoder),
            **self._dataloader_kwargs,
        )

        # ========================================
        # Training and Evaluation
        # ========================================
        try:
            for epoch in range(1, self.training_args.epochs + 1):
                self.model.train(True)
                with torch.enable_grad():
                    train_loss, train_metrics = self.do_epoch(
                        train_data, epoch, "train"
                    )

                self.model.eval()
                with torch.no_grad():
                    test_loss, test_metrics = self.do_epoch(test_data, epoch, "test")

                self.writer.flush()
                if epoch % 5 == 0:
                    logging.info(
                        (
                            f"[{epoch:4d}]\t"
                            f"loss/train={train_loss:2.4f}\t"
                            f"loss/test={test_loss:2.4f}\t"
                            f"f1-score/train={train_metrics['weighted avg']['f1-score']:2.4f}\t"
                            f"f1-score/test={test_metrics['weighted avg']['f1-score']:2.4f}"
                        )
                    )

            if (
                best_epoch_meta["metric_score"]
                < test_metrics["weighted avg"]["f1-score"]
            ):
                best_epoch_meta = {
                    "epoch": epoch,
                    "metric_score": test_metrics["weighted avg"]["f1-score"],
                    "metrics": (train_metrics, test_metrics),
                }
                self.model.save(f"{self._out_dir}/model.pth")

        except KeyboardInterrupt:
            logging.info(
                "Training was interrupted by the user, continuing with reporting and shutdown."
            )

        # ========================================
        # Final Reporting and Clean-Up
        # ========================================
        logging.info(
            (
                f"[{best_epoch_meta['epoch']:4d}]\t"
                f"f1-score/train={best_epoch_meta['metrics'][0]['weighted avg']['f1-score']:2.4f}\t"
                f"f1-score/test={best_epoch_meta['metrics'][1]['weighted avg']['f1-score']:2.4f}"
            )
        )
        self.writer.add_hparams(
            self.training_args.model_dump()
            | {
                "train_len": len(self.dataset.train_set),
                "test_len": len(self.dataset.test_set),
            },
            {
                "f1_train": best_epoch_meta["metrics"][0]["weighted avg"]["f1-score"],
                "f1_test": best_epoch_meta["metrics"][1]["weighted avg"]["f1-score"],
            },
        )

        self.writer.close()

    def do_epoch(
        self,
        dataloader: torch.utils.data.DataLoader,
        epoch_index: int = 0,
        epoch_type: typing.Literal["train", "test"] = "train",
    ):
        epoch_loss: float = 0.0
        out: typing.Dict[str, typing.List] = {"true": [], "pred": []}

        for _, data in enumerate(track(dataloader, transient=True)):
            history, stimulus, action = data

            outputs: torch.Tensor = self.model(history, stimulus)
            loss: torch.Tensor = self.loss_fn(outputs, action.view(-1, 1))

            out["true"].extend(action.tolist())
            out["pred"].extend(outputs.view(-1).round(decimals=0).tolist())

            if epoch_type == "train":
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            epoch_loss += loss.item()

        metrics = classification_report(
            out["true"], out["pred"], output_dict=True, zero_division=0.0
        )

        self.writer.add_scalars(
            epoch_type,
            {
                "loss": epoch_loss / len(dataloader),
                "f1_score": metrics["weighted avg"]["f1-score"],
            },
            global_step=epoch_index,
        )

        return epoch_loss / len(dataloader), metrics

    # ========================================
    # Utility Methods
    # ========================================

    @staticmethod
    def _collate(batch: typing.List[typing.Dict]):
        batch_df: pandas.DataFrame = pandas.DataFrame(batch)

        return (
            torch.concat(
                [
                    torch.stack(batch_df[key].tolist())
                    for key in ["history_1", "history_2"]
                ],
                dim=1,
            ).to("cuda"),
            torch.stack(batch_df["stimulus"].tolist()).to("cuda"),
            torch.Tensor(batch_df["action"].astype(int).tolist()).to("cuda"),
        )

    @pydantic.computed_field
    @property
    def _dataloader_kwargs(self) -> typing.Dict:
        return {
            "batch_size": self.training_args.batch_size,
            "shuffle": True,
            "collate_fn": self._collate,
        }


__all__ = ["Dataset", "Model", "Pipeline"]

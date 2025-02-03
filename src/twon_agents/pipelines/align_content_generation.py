import typing
import os
import pathlib
import random

import pydantic
import rich

import pandas
import datasets
import transformers
import trl
import peft

import twon_agents


class AlignContentGeneration(pydantic.BaseModel):

    class Dataset(pydantic.BaseModel):
        path: str
        eval_frac: float = 0.05
        max_samples: int = 50_000

    class Models(pydantic.BaseModel):
        base: str
        adapter: str

    class Training(pydantic.BaseModel):
        learning_rate: float = 0.00005
        weight_decay: float = 0
        num_train_epochs: int = 8
        per_device_train_batch_size: int = 4
        logging_steps: int = 200

    class Testing(pydantic.BaseModel):
        num_repitions: int = 10
        num_samples: int = 100

    # ---- Main Configuration ----

    task: typing.Literal["post", "reply"]
    dataset: Dataset
    models: Models

    training: Training = Training()
    testing: Testing = Testing()

    do_train: bool = True
    do_eval: bool = True

    peft_args: peft.LoraConfig = peft.LoraConfig(
        r=8,
        lora_alpha=32,
        lora_dropout=0.1,
        task_type="CAUSAL_LM",
    )

    sft_args: trl.SFTConfig | None = None

    # ---- Internal Configuration ----

    _root_path: pathlib.Path = pathlib.Path(os.getcwd())
    _out_dir: str = "models"

    _data_format_fn: typing.Dict[str, callable] = dict(
        post=twon_agents.data.format_post_instructions_dataset,
        reply=twon_agents.data.format_reply_instructions_dataset,
    )

    _metrices_fn: typing.Dict[str, callable] = dict(
        bleu=twon_agents.evaluation.calc_bleu,
        tweeteval_corr=twon_agents.evaluation.calc_tweeteval_corr,
        calc_semantic_distance=twon_agents.evaluation.calc_semantic_distance,
    )

    @pydantic.computed_field
    @property
    def out_path(self) -> pathlib.Path:
        return self._root_path / self._out_dir / self.models.adapter

    def model_post_init(self, __context: typing.Any) -> None:
        if not self.sft_args:
            self.sft_args = trl.SFTConfig(
                **self.training.model_dump(),
                packing=True,
                save_strategy="no",
                evaluation_strategy="steps",
                output_dir=self.out_path,
                push_to_hub=True,
                hub_model_id=self.models.adapter,
            )

        return super().model_post_init(__context)

    def __call__(self):
        dataset: typing.List[typing.Dict] = (
            random.sample(data, self.dataset.max_samples)
            if len(data := self.get_formatted_dataset()) > self.dataset.max_samples
            else data
        )

        train_set, eval_set = self.get_data_splits(dataset)

        # ========================================
        # Train, Evaluate, Push
        # ========================================

        if self.do_train:
            self.train(train_set, eval_set)

        # ========================================
        # Compute Alignment Metrices
        # ========================================

        if self.do_eval:
            self.eval()

        # ========================================
        # Lifecycle End
        # ========================================

    def train(self, train_set: typing.List, eval_set: typing.List):
        trainer: trl.SFTTrainer = trl.SFTTrainer(
            self.models.base,
            args=self.sft_args,
            train_dataset=datasets.Dataset.from_pandas(pandas.DataFrame(train_set)),
            eval_dataset=datasets.Dataset.from_pandas(pandas.DataFrame(eval_set)),
            peft_config=self.peft_args,
        )

        trainer.train()
        trainer.evaluate()
        trainer.save_model(self.out_path)

        if self.sft_args.push_to_hub:
            trainer.push_to_hub()

        del trainer

    def eval(self, eval_set: typing.List):
        pipelines: typing.Dict[str, transformers.Pipeline] = (
            twon_agents.util.load_pipelines(self.models.model_dump())
        )

        eval_samples = [
            random.sample(eval_set, self.testing.num_samples)
            for _ in range(self.testing.num_repitions)
        ]

        generations = [
            twon_agents.util.generated_w_pipelines(pipelines, samples)
            for samples in eval_samples
        ]

        for label, metric_fn in self._metrices_fn.items():
            results: pandas.DataFrame = twon_agents.evaluation.aggregate_runs(
                [metric_fn(samples) for samples in generations]
            )
            (
                results.reset_index().to_json(
                    self.out_path / f"test.{label}.json", indent=4, orient="records"
                )
            )
            rich.print(results)

    # ========================================
    # Utility Methods
    # ========================================

    def get_formatted_dataset(self) -> typing.List[typing.Dict]:
        return self._data_format_fn[self.task](self._root_path / self.dataset.path)

    def get_data_splits(
        self, dataset: typing.List
    ) -> typing.Tuple[typing.List, typing.List]:
        return (
            dataset[: int(len(dataset) * (1 - self.dataset.eval_frac))],
            dataset[-int(len(dataset) * self.dataset.eval_frac) :],
        )

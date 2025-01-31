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

    class Models(pydantic.BaseModel):
        base: str
        adapter: str
    
    class Training(pydantic.BaseModel):
        learning_rate: float = 0.00005
        weight_decay: float = 0
        num_train_epochs: int = 8
        per_device_train_batch_size: int = 4
        logging_steps: int = 50

    class Testing(pydantic.BaseModel):
        num_repitions: int = 10
        num_samples: int = 100


    task: typing.Literal["post", "reply"]
    dataset: str
    dataset_max_samples: int = 50_000
    models: Models

    training: Training = Training()
    testing: Testing = Testing()
    
    peft_args: peft.LoraConfig = peft.LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.1,
        task_type="CAUSAL_LM",
    )

    sft_args: trl.SFTConfig | None = None

    _root_path: pathlib.Path = pathlib.Path(os.getcwd())
    _out_dir: str = "models"

    _data_format_fn = dict(
        post=twon_agents.data.format_post_instructions_dataset,
        reply=twon_agents.data.format_reply_instructions_dataset,
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
                output_dir=self.out_path,
                push_to_hub=True,
                hub_model_id=self.models.adapter
            )

        return super().model_post_init(__context)
    
    def get_formatted_dataset(self) -> typing.List[typing.Dict]:
        return self._data_format_fn[self.task](self._root_path / self.dataset)
    
    def __call__(self):
        self.dataset: typing.List[typing.Dict] = random.sample(self.get_formatted_dataset(), self.dataset_max_samples)

        trainer: trl.SFTTrainer = trl.SFTTrainer(
            self.models.base,
            args=self.sft_args,
            train_dataset=datasets.Dataset.from_pandas(pandas.DataFrame(data=self.dataset)),
            peft_config=self.peft_args,
        )

        trainer.train()

        trainer.save_model(self.out_path)

        if self.sft_args.push_to_hub:
            trainer.push_to_hub()

        del trainer

        pipelines: typing.Dict[str, transformers.Pipeline] = twon_agents.util.load_pipelines(self.models.model_dump())
        rich.print(pipelines)

        test_sets = [random.sample(self.dataset, self.testing.num_samples) for _ in range(self.testing.num_repitions)]

        generations = [
            twon_agents.util.generated_w_pipelines(pipelines, samples)
            for samples in test_sets
        ]

        bleu: pandas.DataFrame = twon_agents.evaluation.aggregate_runs([
            twon_agents.evaluation.calc_bleu(samples)
            for samples in generations
        ])
        bleu.to_json(self.out_path / "test.bleu.json")
        rich.print(bleu)

        tweeteval_corr: pandas.DataFrame = twon_agents.evaluation.aggregate_runs([
            twon_agents.evaluation.calc_tweeteval_corr(samples)
            for samples in generations
        ])
        bleu.to_json(self.out_path / "test.tweeteval_corr.json")
        rich.print(tweeteval_corr)

        rich.print(
            tweeteval_corr.assign(group=list(tweeteval_corr.index.get_level_values(1).str.extract(r"^results.(\w+).\w+")[0]))
            .groupby(["model", "group"])
            .mean()
        )

        semantic_distance: pandas.DataFrame = twon_agents.evaluation.aggregate_runs([
            twon_agents.evaluation.calc_semantic_distance(samples)
            for samples in generations
        ])
        semantic_distance.to_json(self.out_path / "test.semantic_distance.json")
        rich.print(semantic_distance)
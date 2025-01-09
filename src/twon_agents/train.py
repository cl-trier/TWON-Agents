import typing

import pydantic

import pandas

import datasets
import trl
import peft


class Trainer(pydantic.BaseModel):
    name_base_model: str
    name_aligned_model: str
    output_dir: str
        
    train_epochs: int = 8
    batch_size: int = 4

    sft_args: trl.SFTConfig | None = None
    peft_args: peft.LoraConfig | None = None

    def model_post_init(self, __context: typing.Any) -> None:

        if not self.sft_args:
            self.sft_args = trl.SFTConfig(
                num_train_epochs=self.train_epochs,
                per_device_train_batch_size=self.batch_size,
                packing=True, 
                save_strategy="no",
                output_dir=self.output_dir,
                logging_steps=50,
                push_to_hub=True,
                push_to_hub_model_id=self.name_aligned_model
            )

        if not self.peft_args:
            self.peft_args = peft.LoraConfig(
                r=8,
                lora_alpha=16,
                lora_dropout=0.1,
                task_type="CAUSAL_LM",
            )

        return super().model_post_init(__context)


    def __call__(self, train_dataset: typing.List[typing.Dict]) -> None:
        trainer: trl.SFTTrainer = trl.SFTTrainer(
            self.name_base_model,
            args=self.sft_args,
            train_dataset=datasets.Dataset.from_pandas(pandas.DataFrame(data=train_dataset)),
            peft_config=self.peft_args,
        )

        trainer.train()

        trainer.save_model(self.sft_args.output_dir)

        if self.sft_args.push_to_hub:
            trainer.push_to_hub()

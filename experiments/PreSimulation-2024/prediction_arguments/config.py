import dataclasses
import typing


@dataclasses.dataclass
class TrainerConfig:
    num_epochs: int = 5
    batch_size: int = 4
    learning_rate: float = 1e-3


@dataclasses.dataclass
class ClassifierConfig:
    hid_size: int = 128
    dropout: float = 0.2


@dataclasses.dataclass
class Config:
    dataset_path: str = f'../arguments.by.persona.English.parquet'

    encoder: str = 'Twitter/twhin-bert-base'

    data_out_dir: str = f'./data'
    result_dir: str = f'./results'
    test_size: float = 0.2

    text_column: str = 'arguments'
    label_columns: typing.List[str] = dataclasses.field(default_factory=lambda: ['label'])

    trainer_config: TrainerConfig = dataclasses.field(default_factory=TrainerConfig)
    classifier_config: ClassifierConfig = dataclasses.field(default_factory=ClassifierConfig)

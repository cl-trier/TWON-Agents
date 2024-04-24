import pathlib

import pandas as pd
from cltrier_prosem import Pipeline

import config

if __name__ == '__main__':
    CFG = config.Config()

    raw: pd.DataFrame = (
        pd.read_parquet(CFG.dataset_path)
        .pipe(lambda _df: _df.assign(span=pd.Series([[0, 0]] * len(_df))))
        .sample(frac=1.)
    )

    pathlib.Path(CFG.data_out_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(CFG.result_dir).mkdir(parents=True, exist_ok=True)

    train_cut: int = int(len(raw) - len(raw) * CFG.test_size)

    raw[:train_cut].to_parquet(f'{CFG.data_out_dir}/train.parquet')
    raw[train_cut:].to_parquet(f'{CFG.data_out_dir}/test.parquet')

    for label_column in CFG.label_columns:
        result_dir = f'{CFG.result_dir}/{label_column}'
        pathlib.Path(result_dir).mkdir(parents=True, exist_ok=True)

        Pipeline({
            'encoder': {
                'model': CFG.encoder,
            },
            'dataset': {
                'path': CFG.data_out_dir,
                'text_column': CFG.text_column,
                'label_column': label_column,
                'label_classes': list(raw[label_column].unique()),
            },
            'classifier': {
                **CFG.classifier_config.__dict__
            },
            'pooler': {
                'form': 'cls',
                'span_columns': ['span'],
            },
            'trainer': {
                **CFG.trainer_config.__dict__,
                'export_path': result_dir,
            },
        })()

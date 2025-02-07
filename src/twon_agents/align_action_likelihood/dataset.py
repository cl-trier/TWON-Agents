import typing

import pandas
import torch


class Dataset(torch.utils.data.Dataset):
    def __init__(self, df: pandas.DataFrame):
        self.df = df

    def __len__(self):
        return len(self.df)

    def __getitem__(
        self, idx: typing.Union[typing.Dict, slice]
    ) -> typing.Union[typing.Dict, list[typing.Dict]]:
        return self.df.iloc[idx].to_dict()

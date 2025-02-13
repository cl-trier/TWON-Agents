import typing
import collections

import pandas
import torch

from rich.progress import track

from twon_agents.lib import Encoder, functional


class Dataset(torch.utils.data.Dataset):
    def __init__(
        self,
        df: pandas.DataFrame,
        encoder: Encoder | None = None,
        encode_columns: typing.List[str] | None = [
            "history_1",
            "history_2",
            "stimulus",
        ],
    ):
        self.df = df
        self.encoder = encoder
        self.encode_columns = encode_columns

        self.embeds: typing.Dict[str, typing.List[torch.Tensor]] | None = (
            collections.defaultdict(lambda: [])
        )

        if encoder:
            self._preprocess()

    def __len__(self):
        return len(self.df)

    def __getitem__(
        self, idx: typing.Union[typing.Dict, slice]
    ) -> typing.Union[typing.Dict, list[typing.Dict]]:
        if self.encoder:
            return self.df.iloc[idx].to_dict() | {
                label: embed[idx] for label, embed in self.embeds.items()
            }

        return self.df.iloc[idx].to_dict()

    @functional.timeit
    @torch.no_grad()
    def _preprocess(self, batch_size: int = 256):
        def preprocess_step(
            batch: typing.List[typing.Dict],
        ) -> typing.Dict[str, typing.List]:
            batch_df: pandas.DataFrame = pandas.DataFrame(batch)

            return {
                column: self.encoder(batch_df[column].tolist()).cpu()
                for column in self.encode_columns
            }

        for batch in track(
            torch.utils.data.DataLoader(
                self.df.to_dict("records"),
                batch_size=batch_size,
                collate_fn=preprocess_step,
            ),
            transient=True,
            description=f"Encoding {len(self.df)} samples in {len(self.encode_columns)} columns ...",
        ):
            for key, values in batch.items():
                self.embeds[key].extend(values)

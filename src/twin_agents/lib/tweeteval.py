import typing

import clXXXXX_lib
import pandas
import pydantic


class TweetEval(pydantic.BaseModel):
    _threshold: float = 0.0

    def __call__(
        self, source: typing.List[str], target: typing.List[str]
    ) -> typing.Tuple[pandas.Series, pandas.DataFrame]:
        clss_src, clss_tgt = (
            self._preprocess(clXXXXX_lib.classify.Pipeline()(source, self._threshold)),
            self._preprocess(clXXXXX_lib.classify.Pipeline()(target, self._threshold)),
        )

        return (
            TweetEval._calculate_corr(clss_src, clss_tgt),
            TweetEval._calculate_mae(clss_src, clss_tgt),
        )

    @staticmethod
    def _calculate_corr(
        clss_src: pandas.DataFrame, clss_tgt: pandas.DataFrame, method: str = "pearson"
    ) -> pandas.Series:
        return pandas.Series(
            {
                label: src.corr(tgt, method=method)
                for (label, src), (_, tgt) in zip(
                    clss_src.T.iterrows(), clss_tgt.T.iterrows()
                )
            },
            name="correlation",
        )

    @staticmethod
    def _calculate_mae(
        clss_src: pandas.DataFrame, clss_tgt: pandas.DataFrame
    ) -> pandas.DataFrame:
        return (
            (clss_src - clss_tgt)
            .abs()
            .T.agg(["mean", "std"], axis=1)
            .rename(columns={"mean": "error"})
        )

    @staticmethod
    def _preprocess(data: typing.Dict[str, str | float]) -> pandas.DataFrame:
        return pandas.json_normalize([row.model_dump() for row in data]).drop(
            columns=["sample"]
        )

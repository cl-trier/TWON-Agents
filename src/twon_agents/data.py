import typing
import itertools

import pandas 

import cltrier_lib


def filter_tweets(
    df: pandas.DataFrame, 
    min_length: int = 32, 
    remove_w_mentions: bool = True,
    remove_retweets: bool = True
    ) -> pandas.DataFrame:
    return (
        df
        # exclude tweets that start with a mention
        .pipe(lambda _df: _df[~_df["text"].str.startswith("@")] if remove_w_mentions else _df)
        # exclude retweets
        .pipe(lambda _df: _df[~_df["text"].str.contains("RT")] if remove_retweets else _df)
        # exclude tweets with urls
        .pipe(lambda _df: _df[~_df["text"].str.contains("https://")])
        # exclude tweets that are short than 32 characters
        .pipe(lambda _df: _df[_df["text"].str.len() > min_length])
        # remove line breaks 
        .pipe(lambda _df: _df.assign(text=_df["text"].str.replace(r"\n"," ", regex=True)))
    )


def format_post_instructions_dataset(path: str) -> typing.List[typing.Dict]:
    return [
        cltrier_lib.inference.schemas.Chat(messages=[
            cltrier_lib.inference.schemas.Message(role="system", content=f"You are a {row['author_first_name_post']} {row['author_last_name_post']} member of {row['author_party_post']}. Post a Tweet about the following topic:"),
            cltrier_lib.inference.schemas.Message(role="user", content=row["topics_post"]),
            cltrier_lib.inference.schemas.Message(role="assistant", content=row["text_post"])
        ]).model_dump()
        for _, row in pandas.read_csv(path, index_col=0).iterrows()
    ]


def format_reply_instructions_dataset(path: str, n_shots: int = 2) -> typing.List[typing.Dict]:
    return [
            cltrier_lib.inference.schemas.Chat(messages=[
                cltrier_lib.inference.schemas.Message(role="system", content=f"You are a social media user. Respond to the following Tweet based on your last interactions:")
                ] + list(itertools.chain(*[
            [ 
                cltrier_lib.inference.schemas.Message(role="user", content=row.text_post), 
                cltrier_lib.inference.schemas.Message(role="assistant", content=row.text_reply)
            ]
            for row in sample
        ]))).model_dump()
        for _, group in pandas.read_csv(path, index_col=0).groupby("author_id_reply")
        for sample in itertools.combinations(list(group[["text_post", "text_reply"]].itertuples(index=False)), n_shots+1)
        # for sample in [list(group[["text_post", "text_reply"]].itertuples(index=False))[n: n+n_shots+1] for n in range(0, len(group), n_shots+1)]
    ]
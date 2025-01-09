import pandas 


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
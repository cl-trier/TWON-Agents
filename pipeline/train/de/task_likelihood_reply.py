import os

import pandas

from twin_agents.align_action_likelihood import Pipeline


os.environ["CUDA_VISIBLE_DEVICES"] = "2"


if __name__ == "__main__":
    dataset = pandas.read_csv(
        "data/processed/twitter.german.dataset.decision.csv", index_col=[0]
    )

    test_set = dataset.groupby("action").sample(500)
    train_set = dataset.loc[~dataset.index.isin(test_set.index)]

    Pipeline(
        dataset={
            "train_set": train_set,
            "test_set": test_set,
        }
    )()

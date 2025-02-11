import os

import pandas

from twon_agents.align_action_likelihood import Pipeline


os.environ["CUDA_VISIBLE_DEVICES"] = "2"


if __name__ == "__main__":
    Pipeline(
        dataset=dict(
            train_set=pandas.read_csv(
                "data/processed/twitter.german.dataset.decision.csv", index_col=[0]
            ).sample(20000),
            test_set=pandas.read_csv(
                "data/processed/twitter.german.dataset.decision.csv", index_col=[0]
            ).sample(200),
        )
    )()

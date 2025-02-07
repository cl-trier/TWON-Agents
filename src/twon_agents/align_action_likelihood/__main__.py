import os

import pandas

from twon_agents.align_action_likelihood import Pipeline


os.environ["CUDA_VISIBLE_DEVICES"] = "2"


if __name__ == "__main__":
    dummy_data: pandas.DataFrame = pandas.read_csv(
        "data/processed/twitter.german.dataset.decision.csv"
    ).sample(200)

    Pipeline(dataset=dict(train_set=dummy_data, test_set=dummy_data))()

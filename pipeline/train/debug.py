import os

import twin_agents


os.environ["CUDA_VISIBLE_DEVICES"] = "1"

twin_agents.align_content_generation.Pipeline(
    task="reply",
    dataset=dict(
        path="data/processed/twitter.german.dataset.enriched.csv",
        max_samples=50,
        eval_frac=0.2,
    ),
    models=dict(
        base="meta-llama/Llama-3.2-3B-Instruct",
        adapter="XXXXX/twin-Agent-OSN-debug",
    ),
    training=dict(logging_steps=5),
    testing=dict(num_repitions=2, num_samples=5),
)()

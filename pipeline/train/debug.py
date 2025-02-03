import os

import twon_agents


os.environ["CUDA_VISIBLE_DEVICES"] = "1"


twon_agents.pipelines.AlignContentGeneration(
    task="reply",
    dataset=dict(
        path="data/processed/twitter.german.dataset.enriched.csv",
        max_samples=50,
        eval_frac=0.2,
    ),
    models=dict(
        base="meta-llama/Llama-3.2-3B-Instruct",
        adapter="simon-muenker/TWON-Agent-OSN-debug",
    ),
    training=dict(logging_steps=5),
    testing=dict(num_repitions=2, num_samples=5),
)()

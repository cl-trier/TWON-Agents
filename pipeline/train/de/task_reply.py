import os

import twon_agents


os.environ["CUDA_VISIBLE_DEVICES"] = "1"


twon_agents.pipelines.AlignContentGeneration(
    task="reply",
    dataset=dict(
        path="data/processed/twitter.german.dataset.enriched.csv",
    ),
    models=dict(
        base="meta-llama/Llama-3.2-3B-Instruct", 
        adapter="simon-muenker/TWON-Agent-OSN-Replies-de"
    )
)()

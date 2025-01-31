import os

import twon_agents


os.environ["CUDA_VISIBLE_DEVICES"] = "1"


twon_agents.pipelines.AlignContentGeneration(
    task="post",
    dataset="data/processed/twitter.german.dataset.enriched.csv",
    dataset_max_samples=500,
    models=dict(
        base="meta-llama/Llama-3.2-3B-Instruct", 
        adapter="simon-muenker/TWON-Agent-OSN-Post-de"
    ),
    testing=dict(
      num_repitions=10,
      num_samples=100  
    )
)()

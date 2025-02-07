import os

import twon_agents
import twon_agents.align_content_generation


args = twon_agents.align_content_generation.util.pipeline_argparser.parse_args()
os.environ["CUDA_VISIBLE_DEVICES"] = str(args.device)

twon_agents.align_content_generation.Pipeline(
    task="post",
    do_train=args.train,
    do_eval=args.eval,
    dataset=dict(
        path="data/processed/twitter.german.dataset.enriched.csv",
    ),
    models=dict(
        base="meta-llama/Llama-3.2-3B-Instruct",
        adapter="simon-muenker/TWON-Agent-OSN-Post-de",
    ),
)()

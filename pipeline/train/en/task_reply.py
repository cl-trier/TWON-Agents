import os

import twon_agents


args = twon_agents.align_content_generation.util.pipeline_argparser.parse_args()
os.environ["CUDA_VISIBLE_DEVICES"] = str(args.device)

twon_agents.align_content_generation.Pipeline(
    task="reply",
    do_train=args.train,
    do_eval=args.eval,
    dataset=dict(
        path="data/processed/twitter.english.dataset.csv",
    ),
    models=dict(
        base="meta-llama/Llama-3.2-3B-Instruct",
        adapter="simon-muenker/TWON-Agent-OSN-Replies-en",
    ),
)()

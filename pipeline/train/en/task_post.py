import os

import twin_agents


args = twin_agents.align_content_generation.util.pipeline_argparser.parse_args()
os.environ["CUDA_VISIBLE_DEVICES"] = str(args.device)

twin_agents.align_content_generation.Pipeline(
    task="post",
    do_train=args.train,
    do_eval=args.eval,
    dataset=dict(
        path="data/processed/twitter.english.dataset.enriched.csv",
    ),
    models=dict(
        base="meta-llama/Llama-3.2-3B-Instruct",
        adapter="XXXXX/twin-Agent-OSN-Post-en",
    ),
)()

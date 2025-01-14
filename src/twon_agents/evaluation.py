import pandas

import torch
import transformers
import evaluate

from twon_agents import lib


def calc_bleu(predictions: pandas.DataFrame) -> pandas.DataFrame:
    return pandas.DataFrame({
        "base": evaluate.load("bleu").compute(
            references=predictions[("text", "human")].tolist(),
            predictions=predictions[("text", "base")].tolist(),
            smooth=True
        ),
        "adapter": evaluate.load("bleu").compute(
            references=predictions[("text", "human")].tolist(),
            predictions=predictions[("text", "adapter")].tolist(),
            smooth=True
        )
    })


def calc_tweeteval_corr(predictions: pandas.DataFrame) -> pandas.DataFrame:
    return pandas.concat([
        lib.TweetEval()(
            source=predictions[("text", "human")].tolist(),
            target=predictions[("text", "base")].tolist()
        )[0].rename("base"),
        lib.TweetEval()(
            source=predictions[("text", "human")].tolist(),
            target=predictions[("text", "adapter")].tolist()
        )[0].rename("adapter")
    ], axis=1)


def calc_semantic_distance(predictions: pandas.DataFrame) -> pandas.DataFrame:
    tokenizer = transformers.AutoTokenizer.from_pretrained('Twitter/twhin-bert-base')
    model = transformers.AutoModel.from_pretrained('Twitter/twhin-bert-base')

    return pandas.DataFrame({
        "base": [torch.nn.PairwiseDistance()(
            model(**tokenizer(predictions[("text", "human")].tolist(), padding=True, return_tensors="pt")).pooler_output,
            model(**tokenizer(predictions[("text", "base")].tolist(), padding=True, return_tensors="pt")).pooler_output
        ).mean().item()],
        "adapter": [torch.nn.PairwiseDistance()(
            model(**tokenizer(predictions[("text", "human")].tolist(), padding=True, return_tensors="pt")).pooler_output,
            model(**tokenizer(predictions[("text", "adapter")].tolist(), padding=True, return_tensors="pt")).pooler_output
        ).mean().item()]
    }, index=["semantic_distance"])

import pandas

from transformers import AutoTokenizer, AutoModel
from sklearn.decomposition import PCA

import plotly
import plotly.graph_objs as go


def visualize_embeds_3d(predictions: pandas.DataFrame):
    tokenizer = AutoTokenizer.from_pretrained('Twitter/twhin-bert-base')
    transformer = AutoModel.from_pretrained('Twitter/twhin-bert-base')

    for model in ["human", "base", "adapter"]:
        predictions[(model, "text_embeds")] = transformer(**tokenizer(predictions[("text", model)].tolist(), padding=True, return_tensors="pt")).pooler_output.detach().numpy().tolist()
        predictions[(model, "text_embeds_d3")] = list(PCA(n_components=3).fit_transform(predictions[(model, "text_embeds")].tolist()))

    plotly.offline.iplot(
        go.Figure(
            data=[
                    go.Scatter3d(
                    **{
                        dim: group["value"].str[idx].tolist() 
                        for idx, dim in enumerate(["x", "y", "z"])
                    },
                    name=label,
                    mode='markers',
                    marker={
                        'size': 6,
                        'opacity': 0.8,
                    }
                )
                for label, group in (
                    predictions
                    .melt()
                    .rename(columns={None: "population"})
                    .pipe(lambda _df: _df[_df["model"] == "text_embeds"])
                    .groupby("population")
                )
            ], 
            layout=go.Layout(
                margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
                height=820
            )
        )
    )
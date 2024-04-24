import typing 

import numpy as np
import pandas as pd
import matplotlib as mpl
import seaborn as sns

import torch


cat = "label"

data = pd.concat([
	pd.read_parquet(f'results/{cat}/embeds.train.parquet'),
	pd.read_parquet(f'results/{cat}/embeds.test.parquet')
])

dist = torch.nn.PairwiseDistance()

results: typing.Dict[typing.Tuple[str, str], float] = {}


for model_1, c_1 in data.groupby(cat)['embeds']:
    for model_2, c_2 in data.groupby(cat)['embeds']:

        if (
            (model_1, model_2) in results.keys() or 
            (model_2, model_1) in results.keys()
        ):
            continue

        res = sum([
            sum(dist(
                torch.tensor(np.array(v_1)), 
                torch.tensor(np.array(c_2.tolist()))
                )) / len(c_2)
            for v_1 in c_1
        ]) / len(c_1)

        results[(model_1, model_2)] = res

        print(f'{model_1}:{model_2}:{res.item()}')

matrix = pd.DataFrame([{f'{cat}_1': key[0], f'{cat}_2': key[1], 'distance': value.item()} for key, value in results.items()]).pivot(index=f'{cat}_1', columns=f'{cat}_2', values='distance').T
print(matrix)

sns.heatmap(
    matrix,
    annot=True,
    fmt='g',
    linewidth=.5,
    )
mpl.pyplot.savefig(f'results/{cat}/plot.heat.embed.distance.pdf', format='pdf')

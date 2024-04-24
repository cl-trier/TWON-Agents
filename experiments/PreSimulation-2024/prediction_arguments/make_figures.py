import numpy as np
import pandas as pd
import matplotlib as mpl
import seaborn as sns

from sklearn.decomposition import PCA

cat = "label"


data = pd.concat([
	pd.read_parquet(f'results/{cat}/embeds.train.parquet'),
	pd.read_parquet(f'results/{cat}/embeds.test.parquet')
])

data[['x', 'y']] = [(emb[0], emb[1]) for emb in PCA(n_components=2).fit_transform(np.stack(data.embeds.tolist()))]

sns.scatterplot(data, x='x', y='y', hue=cat)
mpl.pyplot.savefig(f'results/{cat}/plot.pca.scatter.pdf', format='pdf')
mpl.pyplot.close()

grid = sns.FacetGrid(data, col=cat, hue=cat)
grid.map_dataframe(sns.kdeplot, x='x', y='y', fill=True)
mpl.pyplot.savefig(f'results/{cat}/plot.pca.kde.pdf', format='pdf')
mpl.pyplot.close()

sns.heatmap(
	pd.read_csv(f'results/{cat}/metric.cross_tabulation.csv', index_col=[0]).T,
	annot=True,
    fmt='g',
    linewidth=.5,
)
mpl.pyplot.savefig(f'results/{cat}/plot.heat.embed.classification.pdf', format='pdf')
mpl.pyplot.close()

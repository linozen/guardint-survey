#!/usr/bin/env python3

import plotly.express as px
import pandas as pd

# Import dataframes
df_all = pd.read_pickle("data/all.pkl")
df_media = pd.read_pickle("data/media.pkl")

df_corr_all = df_all.corr(method="pearson")
df_corr_media = df_media.corr(method="pearson")

fig = px.imshow(df_corr_media)
fig.show()

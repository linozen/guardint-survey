#!/usr/bin/env python3

import pandas as pd
import phik

# Import dataframes
df_merged = pd.read_pickle("data/merged.pkl")
df_media = pd.read_pickle("data/media.pkl")
df_civsoc = pd.read_pickle("data/civsoc.pkl")


def save_corr_matrix(df, name):
    corr = df.phik_matrix()
    corr.to_pickle(f"./data/{name}.pkl")
    corr.to_excel(f"./data/{name}.xlsx")
    corr.to_csv(f"./data/{name}.csv")


def save_sig_matrix(df, name):
    sig = df.significance_matrix(significance_method="asymptotic")
    sig.to_pickle(f"./data/{name}.pkl")
    sig.to_excel(f"./data/{name}.xlsx")
    sig.to_csv(f"./data/{name}.csv")


df_corr_merged = save_corr_matrix(df_merged, "merged_corr")
df_corr_media = save_corr_matrix(df_media, "media_corr")
df_corr_civsoc = save_corr_matrix(df_civsoc, "civsoc_corr")

df_corr_merged = save_sig_matrix(df_merged, "merged_sig")
df_corr_media = save_sig_matrix(df_media, "media_sig")
df_corr_civsoc = save_sig_matrix(df_civsoc, "civsoc_sig")

#!/usr/bin/env python3

import pandas as pd
from pandas_profiling import ProfileReport

# Import dataframes
df_merged = pd.read_pickle("data/merged.pkl")
df_media = pd.read_pickle("data/media.pkl")
df_civsoc = pd.read_pickle("data/civsoc.pkl")

# Generate profiles
merged_profile = ProfileReport(df_merged, config_file="profiles/profile_merged.yml")
merged_profile.to_file("profiles/merged.html")

media_profile = ProfileReport(df_media, config_file="profiles/profile_media.yml")
media_profile.to_file("profiles/media.html")

civsoc_profile = ProfileReport(df_civsoc, config_file="profiles/profile_civsoc.yml")
civsoc_profile.to_file("profiles/civsoc.html")

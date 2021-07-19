#!/usr/bin/env python3

import pandas as pd
from pandas_profiling import ProfileReport

# Import dataframes
df_all = pd.read_pickle("data/all.pkl")
df_media = pd.read_pickle("data/media.pkl")
df_civsoc = pd.read_pickle("data/civsoc.pkl")

# Generate profiles
all_profile = ProfileReport(df_all, config_file="profiles/profile_all.yml")
all_profile.to_file("profiles/all.html")

media_profile = ProfileReport(df_media, config_file="profiles/profile_media.yml")
media_profile.to_file("profiles/media.html")

civsoc_profile = ProfileReport(df_civsoc, config_file="profiles/profile_civsoc.yml")
civsoc_profile.to_file("profiles/civsoc.html")

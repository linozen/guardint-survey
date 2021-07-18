#!/usr/bin/env python3

import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

# Import dataframes
df_all = pd.read_pickle("data/all.pkl")
df_media = pd.read_pickle("data/media.pkl")

# Generate profiles
media_profile = ProfileReport(df_media, config_file="profile.yml")
media_profile.to_file("profiles/media.html")

all_profile = ProfileReport(df_all, config_file="profile.yml")
all_profile.to_file("profiles/all.html")

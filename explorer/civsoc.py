#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="GUARDINT Civil Society Scrutiny Survey Data Explorer",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("GUARDINT Civil Society Scrutiny Survey Data Explorer")


@st.cache
def get_data():
    df = pd.read_csv("../data/civsoc.csv", sep=",")
    df = df.fillna("No answer")
    unwanted = ["Consentform.", "seed.", "submitdate.", "id."]
    for startstring in unwanted:
        unwanted_column = df.columns[df.columns.str.startswith(startstring)]
        df.drop(unwanted_column, axis=1, inplace=True)
    return df


# Disply the raw data
df = get_data()
st.dataframe(df, height=1000)

# Factors to filter by (CS only)
# ------------------------------
# CShr1-2
# CSattitude1-6
# CSgender

# Factors to compare (CS only)
# ------------------------------
# CSfinance2-4
# CSpreselection
# CScampact1-2
# CScamptrans1-2
# CScampimpact1-2
# CSadvocact1-2
# CSadvoctrans1-2
# CSadvocimpact1-2
# CSlitigateact1-2
# CSlitigatecost1-3
# CSlitigatetrans1-2
# CSlitigateimpact1-2
# CScontraintself1

# Filter logic
gender = st.sidebar.selectbox("Self-identified Gender", ["All", "Woman", "Man"])

"You selected: ", gender

if gender == "All":
    df_filtered = df
else:
    df_filtered = df[df["CSgender. Gender: How do you identify?"] == gender]

# Display dynamic charts
st.header("3. Policy Advocacy")
st.subheader("Transnational Scope")

st.text(
    "How frequently does your policy advocacy address transnational issues of surveillance by intelligence agencies? [CSadvoctrans1]"
)

CSadvoctrans1_df = df_filtered.loc[:, df.columns.str.startswith("CSadvoctrans1.")]
CSadvoctrans1_labels = list(set(CSadvoctrans1_df.values.flatten().tolist()))
CSadvoctrans1_counts = CSadvoctrans1_df.value_counts()
CSadvoctrans1_fig = px.pie(
    df_filtered, values=CSadvoctrans1_counts, names=CSadvoctrans1_labels
)
st.plotly_chart(CSadvoctrans1_fig)

st.text(
    "When performing policy advocacy concerning surveillance by intelligence agencies, how often do you collaborate with civil society actors in other countries? [CSadvoctrans2]"
)

CSadvoctrans2_df = df_filtered.loc[:, df.columns.str.startswith("CSadvoctrans2.")]
CSadvoctrans2_labels = list(set(CSadvoctrans1_df.values.flatten().tolist()))
CSadvoctrans2_counts = CSadvoctrans2_df.value_counts()
CSadvoctrans2_fig = px.pie(
    df_filtered, values=CSadvoctrans2_counts, names=CSadvoctrans2_labels
)
st.plotly_chart(CSadvoctrans2_fig)

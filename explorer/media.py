#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="GUARDINT Media Scrutiny Survey Data Explorer",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('GUARDINT Media Scrutiny Survey Data Explorer')

@st.cache
def get_data():
    df = pd.read_csv("../data/media.csv", sep=",")
    df = df.fillna("No answer")
    unwanted = ["Consentform.", "seed.", "submitdate.", "id."]
    for startstring in unwanted:
        unwanted_column = df.columns[df.columns.str.startswith(startstring)]
        df.drop(unwanted_column, axis=1, inplace=True)
    return df


df = get_data()
st.dataframe(df, height=1000)

gender = st.sidebar.selectbox(
    "Self-identified Gender",
    ['All', 'Woman', 'Man']
)

"You selected: ", gender

if gender == 'All':
    df_by_gender = df
else:
    df_by_gender = df[df["MSgender. Gender: How do you identify?"] == gender]

st.subheader("Employment status [MShr1]")
labels = df_by_gender["MShr1. What is your employment status?"].unique()
counts = df_by_gender["MShr1. What is your employment status?"].value_counts()
fig = px.pie(df_by_gender, values=counts, names=labels)

st.plotly_chart(fig)

st.subheader("Enough time to cover surveillance by intelligence agencies? [MShr2]")

labels_long = df_by_gender[
    "MShr4. Within the past year, did you have enough time to cover surveillance by intelligence agencies?"
].unique().tolist()

labelsMShr2 = []
for label in labels_long:
    l = label.split("(")[0]
    labelsMShr2.append(l)

countsMShr2 = df_by_gender[
    "MShr4. Within the past year, did you have enough time to cover surveillance by intelligence agencies?"
].value_counts()

figMShr2 = px.pie(df_by_gender, values=countsMShr2, names=labelsMShr2)
st.plotly_chart(figMShr2)

#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
st.write("### Survey Data Explorer (Media)", df)

option = st.selectbox(
    "Self-identified Gender", df["MSgender. Gender: How do you identify?"].unique()
)

"You selected: ", option

df_by_gender = df[df["MSgender. Gender: How do you identify?"] == option]

st.subheader("Employment status [MShr1]")
labels = df_by_gender["MShr1. What is your employment status?"].unique()
counts = df_by_gender["MShr1. What is your employment status?"].value_counts()

fig, ax = plt.subplots()
ax.pie(counts, labels=labels)

st.pyplot(fig)

st.subheader("Enough time to cover surveillance by intelligence agencies? [MShr1]")
labels1 = df_by_gender[
    "MShr4. Within the past year, did you have enough time to cover surveillance by intelligence agencies?"
].unique()
counts1 = df_by_gender[
    "MShr4. Within the past year, did you have enough time to cover surveillance by intelligence agencies?"
].value_counts()

fig1, ax1 = plt.subplots()
ax1.pie(counts1, labels=labels1)

st.pyplot(fig1)

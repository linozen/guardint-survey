import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


###################################################################################
# General configuration
###################################################################################
st.set_page_config(
    page_title="GUARDINT Media Scrutiny Survey Data Explorer",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("GUARDINT Media Scrutiny Survey Data Explorer")


###################################################################################
# Data acquisition
###################################################################################
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

# Factors to filter by (MS only)
# ------------------------------
# MShr1-2
# MSattitude1-6
# MSgender

# Factors to compare (MS only)
# ------------------------------
# MShr3-4
# MSapp1-2
# MSsoc1-6
# MStrans1-3
# MSimpact1-2
# MSprotectrta1-6
# MSconstraintbylaw1-4
# MScontraintself1

###################################################################################
# Filtering
###################################################################################
gender = st.sidebar.selectbox("Self-identified Gender", ["All", "Woman", "Man"])

"You selected: ", gender

if gender == "All":
    df_by_gender = df
else:
    df_by_gender = df[df["MSgender. Gender: How do you identify?"] == gender]


###################################################################################
# Display
###################################################################################
st.subheader("Employment status [MShr1]")
labels = df_by_gender["MShr1. What is your employment status?"].unique()
counts = df_by_gender["MShr1. What is your employment status?"].value_counts()
fig = px.pie(df_by_gender, values=counts, names=labels)

st.plotly_chart(fig)

st.subheader("Enough time to cover surveillance by intelligence agencies? [MShr2]")

labels_long = (
    df_by_gender[
        "MShr4. Within the past year, did you have enough time to cover surveillance by intelligence agencies?"
    ]
    .unique()
    .tolist()
)

labelsMShr2 = []
for label in labels_long:
    l = label.split("(")[0]
    labelsMShr2.append(l)

countsMShr2 = df_by_gender[
    "MShr4. Within the past year, did you have enough time to cover surveillance by intelligence agencies?"
].value_counts()

figMShr2 = px.pie(df_by_gender, values=countsMShr2, names=labelsMShr2)
st.plotly_chart(figMShr2)

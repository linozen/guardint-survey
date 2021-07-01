import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import glob

# Factors to filter by (CS & MS)
# --------------------------------------------
# country
# ----------------------+---------------------
# CShr1                 | MShr1               hr1
# CSattitude1-6         | MSattitude1-6       attitude1-2
# CSgender              | MSgender            gender

# Factors to compare (CS & MS)
# ----------------------+---------------------
# CShr2                 | MShr2
# CSexpertise1-4        | MSexpertise1-4
# CSfinance1            | MSfinance1
# CSfoi1-4              | MSfoi1-4
# CSprotectops1-4       | MSprotectops1-4
# CSprotectleg1-3       | MSprotectleg1-3
# CSconstraintinter1-6  | MSconstraintinter1-6

###################################################################################
# General configuration
###################################################################################
st.set_page_config(
    page_title="IOI Survey Data Explorer (CS & MS)",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("IOI Survey Data Explorer (CS & MS)")


###################################################################################
# Data wrangling
###################################################################################
@st.cache
def get_merged_cs_df():

    # Merge CSV files into DataFrame
    cs_csv_files = [
        "data/cs_uk_short.csv",
        "data/cs_de_short.csv",
        "data/cs_fr_short.csv",
    ]
    df_list = []
    for csv in cs_csv_files:
        df_list.append(pd.read_csv(csv, sep=";"))
    df = pd.concat(df_list)

    # Use startlanguage as country column
    df = df.rename(columns={"startlanguage": "XXcountry", "lastpage": "XXlastpage"})
    df = df.replace(to_replace=r"en", value="United Kingdom")
    df = df.replace(to_replace=r"de", value="Germany")
    df = df.replace(to_replace=r"fr", value="France")

    # Drop (very) incomplete surveys
    df = df[df["XXlastpage"] > 2]

    # Drop all but the columns needed for the analysis
    df = df[
        [
            "XXcountry",
            "XXlastpage",
            "CShr1",
            "CShr2",
            "CSgender",
            "CSexpertise1",
            "CSexpertise2",
            "CSexpertise3",
            "CSexpertise4",
            "CSfinance1",
            "CSfoi1",
            "CSfoi2",
            "CSfoi3",
            "CSfoi4",
            "CSprotectops2",
            "CSprotectops4",
            "CSprotectleg1",
            "CSprotectleg2",
            "CSconstraintinter1",
            "CSconstraintinter2",
            "CSconstraintinter3",
            "CSattitude1",
            "CSattitude2",
        ]
    ]

    # Make column names compatible
    df.columns = df.columns.str[2:]

    # Set surveytype
    df["surveytype"] = "Civil Society Scrutiny"
    return df


@st.cache
def get_merged_ms_df():
    # Merge CSV files into DataFrame
    ms_csv_files = [
        "data/ms_uk_short.csv",
        "data/ms_de_short.csv",
        "data/ms_fr_short.csv",
    ]
    df_list = []
    for csv in ms_csv_files:
        df_list.append(pd.read_csv(csv, sep=";"))
    df = pd.concat(df_list)

    # Use startlanguage as country column and correct column names
    df = df.rename(
        columns={
            "startlanguage": "XXcountry",
            "lastpage": "XXlastpage",
            "MFfoi2": "MSfoi2",
            "MScontstraintinter1": "MSconstraintinter1",
            "MSprotectleg2A": "MSprotectleg2",
        }
    )
    df = df.replace(to_replace=r"en", value="United Kingdom")
    df = df.replace(to_replace=r"de", value="Germany")
    df = df.replace(to_replace=r"fr", value="France")

    # Drop (very) incomplete surveys
    df = df[df["XXlastpage"] > 2]

    # Drop all but the columns needed for the analysis
    df = df[
        [
            "XXcountry",
            "XXlastpage",
            "MShr1",
            "MShr2",
            "MSgender",
            "MSexpertise1",
            "MSexpertise2",
            "MSexpertise3",
            "MSexpertise4",
            "MSfinance1",
            "MSfoi1",
            "MSfoi2",
            "MSfoi3",
            "MSfoi4",
            "MSprotectops2",
            "MSprotectops4",
            "MSprotectleg1",
            "MSprotectleg2",
            "MSconstraintinter1",
            "MSconstraintinter2",
            "MSconstraintinter3",
            "MSattitude1",
            "MSattitude2",
        ]
    ]

    # Make column names compatible
    df.columns = df.columns.str[2:]

    # Set surveytype
    df["surveytype"] = "Media Scrutiny"
    return df


###################################################################################
# Merge CS with MS
###################################################################################
df_cs = get_merged_cs_df()
df_ms = get_merged_ms_df()
df = pd.concat([df_cs, df_ms], ignore_index=True)

###################################################################################
# Make answers human-readable
###################################################################################
df["hr1"] = df["hr1"].replace(
    {
        "AO01": "Full-time",
        "AO02": "Part-time (>50%)",
        "AO03": "Part-time (<50%)",
        "AO04": "Freelance",
        "AO05": "Unpaid",
        "AO06": "Other",
        "AO07": "Other",
    }
)

df["gender"] = df["gender"].fillna("Other")
df["gender"] = df["gender"].replace(
    {
        "AO01": "Female",
        "AO02": "Non-binary",
        "AO03": "Male",
        "AO04": "Other",
    }
)

df["expertise2"] = df["expertise2"].replace(
    {
        "AO01": "Expert knowledge",
        "AO02": "Advanced knowledge",
        "AO03": "Some knowledge",
        "AO04": "Basic knowledge",
        "AO05": "No knowledge",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["expertise3"] = df["expertise3"].replace(
    {
        "AO01": "Expert knowledge",
        "AO02": "Advanced knowledge",
        "AO03": "Some knowledge",
        "AO04": "Basic knowledge",
        "AO05": "No knowledge",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["expertise4"] = df["expertise4"].replace(
    {
        "AO01": "Expert knowledge",
        "AO02": "Advanced knowledge",
        "AO03": "Some knowledge",
        "AO04": "Basic knowledge",
        "AO05": "No knowledge",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["finance1"] = df["finance1"].replace(
    {
        "AO01": "A great deal of funding",
        "AO02": "Sufficient funding",
        "AO03": "Some funding",
        "AO04": "Little funding",
        "AO05": "No funding",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["foi1"] = df["foi1"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

df["foi3"] = df["foi3"].replace(
    {
        "AO01": "Yes, within 30 days",
        "AO02": "No, usually longer than 30 days",
        "AO03": "Never",
        "AO04": "I don't know",
        "AO05": "I prefere not to say",
    }
)

is_civsoc = df.surveytype == "Civil Society Scrutiny"
df.loc[is_civsoc, "foi4"] = df["foi4"].replace(
    {
        "AO01": "Very helpful",
        "AO03": "Helpful in parts",
        "AO05": "Not helpful at all",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)
is_not_civsoc = df.surveytype == "Media Scrutiny"
df.loc[is_not_civsoc, "foi4"] = df["foi4"].replace(
    {
        "AO01": "Very helpful",
        "AO02": "Helpful in parts",
        "AO03": "Not helpful at all",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)


###################################################################################
# Make answers analysable
###################################################################################
df["hr2"] = df["hr2"].replace("?", np.nan)
df["hr2"] = df["hr2"].replace("0,5", 0.5)
df["hr2"] = pd.to_numeric(df["hr2"], errors="coerce")

df["foi2"] = df["foi2"].replace({"20+": 20.0, " ca 10": 10.0, "15+": 15.0})
df["foi2"] = pd.to_numeric(df["foi2"], errors="coerce")

###################################################################################
# Filter logic
###################################################################################
filters = {
    "surveytype": st.sidebar.selectbox(
        "Survey type", ["All", "Civil Society Scrutiny", "Media Scrutiny"]
    ),
    "country": st.sidebar.selectbox(
        "Country", ["All", "United Kingdom", "Germany", "France"]
    ),
    "hr1": st.sidebar.selectbox(
        "Employment status",
        [
            "All",
            "Full-time",
            "Part-time (>50%)",
            "Part-time (<50%)",
            "Freelance",
            "Unpaid",
            "Other",
        ],
    ),
    "gender": st.sidebar.selectbox(
        "Self-identified gender",
        [
            "All",
            "Female",
            "Non-binary",
            "Male",
            "Other",
        ],
    ),
}

filter = np.full(len(df.index), True)
for column_name, selectbox in filters.items():
    if selectbox == "All":
        continue
    else:
        filter = filter & (df[column_name] == selectbox)
    print(filter)

###################################################################################
# Display table
###################################################################################
st.dataframe(df[filter], height=1000)

###################################################################################
# Display dynamic charts
###################################################################################
# Histogram (hr2)
st.write(
    "How many days per month do you work on surveillance by intelligence agencies? `[hr2]`"
)
hr2_fig = px.histogram(
    df[filter], x="hr2", labels={"hr2": "days per month"}, color="country"
)
st.plotly_chart(hr2_fig)

# Histogram (expertise1)
st.write(
    "How many years have you spent working on surveillance by intelligence agencies? `[expertise1]`"
)
expertise1_fig = px.histogram(
    df[filter],
    x="expertise1",
    labels={"expertise1": "years"},
    color="country",
)
st.plotly_chart(expertise1_fig)

# Pie chart (expertise2)
st.write(
    "How do you assess your level of expertise concerning the **legal** aspects of surveillance by intelligence agencies? For example, knowledge of intelligence law, case law. `[expertise2]`"
)
expertise2_counts = df[filter]["expertise2"].value_counts()
expertise2_labels = df[filter]["expertise2"].dropna().unique().tolist()
expertise2_fig = px.pie(
    df[filter],
    values=expertise2_counts,
    names=expertise2_labels,
    color_discrete_sequence=px.colors.qualitative.Dark2,
)
st.plotly_chart(expertise2_fig)

# Pie chart (expertise3)
st.write(
    "How do you assess your level of expertise concerning the **political** aspects of surveillance by intelligence agencies?` [expertise3]`"
)
expertise3_counts = df[filter]["expertise3"].value_counts()
expertise3_labels = df[filter]["expertise3"].dropna().unique().tolist()
expertise3_fig = px.pie(
    df[filter],
    values=expertise3_counts,
    names=expertise3_labels,
    color_discrete_sequence=px.colors.qualitative.Dark2,
)
st.plotly_chart(expertise3_fig)

# Pie chart (expertise4)
st.write(
    "How do you assess your level of expertise concerning the **technical** aspects of surveillance by intelligence agencies?` [expertise4]`"
)
expertise4_counts = df[filter]["expertise4"].value_counts()
expertise4_labels = df[filter]["expertise4"].dropna().unique().tolist()
expertise4_fig = px.pie(
    df[filter],
    values=expertise4_counts,
    names=expertise4_labels,
    color_discrete_sequence=px.colors.qualitative.Dark2,
)
st.plotly_chart(expertise4_fig)

# Pie Chart (finance1)
st.write(
    "How do you assess the financial resources that have been available for your work on intelligence over the past 5 years? `[finance1]`"
)
finance1_counts = df[filter]["finance1"].value_counts()
finance1_labels = df[filter]["finance1"].dropna().unique().tolist()
finance1_fig = px.pie(
    df[filter],
    values=finance1_counts,
    names=finance1_labels,
    color_discrete_sequence=px.colors.qualitative.Dark2,
)
st.plotly_chart(finance1_fig)

# Pie Chart (foi1)
st.write(
    "Have you requested information under the national Freedom of Information Law  when you worked on intelligence-related issues over the past 5 years? `[foi1]`"
)
foi1_counts = df[filter]["foi1"].value_counts()
foi1_labels = df[filter]["foi1"].dropna().unique().tolist()
foi1_fig = px.pie(
    df[filter],
    values=foi1_counts,
    names=foi1_labels,
    color_discrete_sequence=px.colors.qualitative.Dark2,
)
st.plotly_chart(foi1_fig)

# Histogram (foi2)
st.write("How often did you request information? `[foi2]`")
foi2_fig = px.histogram(
    df[filter],
    x="foi2",
    nbins=3,
    labels={"foi2": "Number of requests"},
    color="country",
)
st.plotly_chart(foi2_fig)

# Pie Chart (foi3)
st.write(
    "Over the past 5 years, did you receive a response to your FOI request(s) in a timely manner? `[foi3]`"
)
foi3_counts = df[filter]["foi3"].value_counts()
foi3_labels = df[filter]["foi3"].dropna().unique().tolist()
foi3_fig = px.pie(
    df[filter],
    values=foi3_counts,
    names=foi3_labels,
    color_discrete_sequence=px.colors.qualitative.Dark2,
)
st.plotly_chart(foi3_fig)

# Pie Chart (foi4)
st.write(
    "How helpful have Freedom of Information requests been for your work on intelligence-related issues? `[foi4]`"
)
foi4_counts = df[filter]["foi4"].value_counts()
foi4_labels = df[filter]["foi4"].dropna().unique().tolist()
foi4_fig = px.pie(
    df[filter],
    values=foi4_counts,
    names=foi4_labels,
    color_discrete_sequence=px.colors.qualitative.Dark2,
)
st.plotly_chart(foi4_fig)

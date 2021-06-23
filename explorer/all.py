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
# CShr1-2               | MShr1-2
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
# Data acquisition
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
# Filter logic
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

# TODO build surveytype filter

for column_name, selectbox in filters.items():
    if selectbox == "All":
        continue
    else:
        filter = filter & (df[column_name] == selectbox)
    print(filter)


st.dataframe(df[filter], height=1000)

# Display dynamic charts
# st.header("3. Policy Advocacy")
# st.subheader("Transnational Scope")

# st.text(
#     "How frequently does your policy advocacy address transnational issues of surveillance by intelligence agencies? [CSadvoctrans1]"
# )

# CSadvoctrans1_df = df_filtered.loc[:, df.columns.str.startswith("CSadvoctrans1.")]
# CSadvoctrans1_labels = list(set(CSadvoctrans1_df.values.flatten().tolist()))
# CSadvoctrans1_counts = CSadvoctrans1_df.value_counts()
# CSadvoctrans1_fig = px.pie(
#     df_filtered, values=CSadvoctrans1_counts, names=CSadvoctrans1_labels
# )
# st.plotly_chart(CSadvoctrans1_fig)

# st.text(
#     "When performing policy advocacy concerning surveillance by intelligence agencies, how often do you collaborate with civil society actors in other countries? [CSadvoctrans2]"
# )

# CSadvoctrans2_df = df_filtered.loc[:, df.columns.str.startswith("CSadvoctrans2.")]
# CSadvoctrans2_labels = list(set(CSadvoctrans1_df.values.flatten().tolist()))
# CSadvoctrans2_counts = CSadvoctrans2_df.value_counts()
# CSadvoctrans2_fig = px.pie(
#     df_filtered, values=CSadvoctrans2_counts, names=CSadvoctrans2_labels
# )
# st.plotly_chart(CSadvoctrans2_fig)

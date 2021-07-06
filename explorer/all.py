import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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
# CSprotectops2-4       | MSprotectops2-4
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

    # Rename columns
    df = df.rename(
        columns={
            "startlanguage": "XXcountry",
            "lastpage": "XXlastpage",
            "CSprotectops1[SQ01]": "CSprotectops1[sectraining]",
            "CSprotectops1[SQ02]": "CSprotectops1[e2e]",
            "CSprotectops3[SQ01]": "CSprotectops3[encrypted_email]",
            "CSprotectops3[SQ02]": "CSprotectops3[vpn]",
            "CSprotectops3[SQ03]": "CSprotectops3[tor]",
            "CSprotectops3[SQ04]": "CSprotectops3[e2e_chat]",
            "CSprotectops3[SQ05]": "CSprotectops3[encrypted_hardware]",
            "CSprotectops3[SQ06]": "CSprotectops3[2fa]",
            "CSprotectops3[SQ07]": "CSprotectops3[other]",
            "CSprotectleg3[SQ01]": "CSprotectleg3[free_counsel]",
            "CSprotectleg3[SQ02]": "CSprotectleg3[cost_insurance]",
            "CSprotectleg3[SQ03]": "CSprotectleg3[other]",
            "CSconstraintinter4[SQ01]": "CSconstraintinter4[police_search]",
            "CSconstraintinter4[SQ02]": "CSconstraintinter4[seizure]",
            "CSconstraintinter4[SQ03]": "CSconstraintinter4[extortion]",
            "CSconstraintinter4[SQ04]": "CSconstraintinter4[violent_threat]",
            "CSconstraintinter4[SQ05]": "CSconstraintinter4[inspection_during_travel]",
            "CSconstraintinter4[SQ06]": "CSconstraintinter4[detention]",
            "CSconstraintinter4[SQ07]": "CSconstraintinter4[surveillance_signalling]",
            "CSconstraintinter4[SQ08]": "CSconstraintinter4[online_harassment]",
            "CSconstraintinter4[SQ09]": "CSconstraintinter4[entry_on_deny_lists]",
            "CSconstraintinter4[SQ10]": "CSconstraintinter4[exclusion_from_events]",
            "CSconstraintinter4[SQ11]": "CSconstraintinter4[public_defamation]",
            "CSconstraintinter5[SQ01]": "CSconstraintinter5[unsolicited_information]",
            "CSconstraintinter5[SQ02]": "CSconstraintinter5[invitations]",
            "CSconstraintinter5[SQ03]": "CSconstraintinter5[other]",
            "CSconstraintinter6[SQ01]": "CSconstraintinter6[gender]",
            "CSconstraintinter6[SQ02]": "CSconstraintinter6[ethnicity]",
            "CSconstraintinter6[SQ03]": "CSconstraintinter6[political]",
            "CSconstraintinter6[SQ04]": "CSconstraintinter6[sexual]",
            "CSconstraintinter6[SQ05]": "CSconstraintinter6[religious]",
            "CSconstraintinter6[SQ06]": "CSconstraintinter6[other]",
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
            "CSprotectops1[sectraining]",
            "CSprotectops1[e2e]",
            "CSprotectops2",
            "CSprotectops3[encrypted_email]",
            "CSprotectops3[vpn]",
            "CSprotectops3[tor]",
            "CSprotectops3[e2e_chat]",
            "CSprotectops3[encrypted_hardware]",
            "CSprotectops3[2fa]",
            "CSprotectops3[other]",
            "CSprotectops4",
            "CSprotectleg1",
            "CSprotectleg2",
            "CSprotectleg3[free_counsel]",
            "CSprotectleg3[cost_insurance]",
            "CSprotectleg3[other]",
            "CSconstraintinter1",
            "CSconstraintinter2",
            "CSconstraintinter3",
            "CSconstraintinter4[police_search]",
            "CSconstraintinter4[seizure]",
            "CSconstraintinter4[extortion]",
            "CSconstraintinter4[violent_threat]",
            "CSconstraintinter4[inspection_during_travel]",
            "CSconstraintinter4[detention]",
            "CSconstraintinter4[surveillance_signalling]",
            "CSconstraintinter4[online_harassment]",
            "CSconstraintinter4[entry_on_deny_lists]",
            "CSconstraintinter4[exclusion_from_events]",
            "CSconstraintinter4[public_defamation]",
            "CSconstraintinter5[unsolicited_information]",
            "CSconstraintinter5[invitations]",
            "CSconstraintinter5[other]",
            "CSconstraintinter6[gender]",
            "CSconstraintinter6[ethnicity]",
            "CSconstraintinter6[political]",
            "CSconstraintinter6[sexual]",
            "CSconstraintinter6[religious]",
            "CSconstraintinter6[other]",
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

    # Rename columns
    df = df.rename(
        columns={
            "startlanguage": "XXcountry",
            "lastpage": "XXlastpage",
            "MFfoi2": "MSfoi2",
            "MScontstraintinter1": "MSconstraintinter1",
            "MSprotectleg2A": "MSprotectleg2",
            "MSprotectops1[SQ01]": "MSprotectops1[sectraining]",
            "MSprotectops1[SQ03]": "MSprotectops1[e2e]",
            "MSprotectops3[SQ01]": "MSprotectops3[encrypted_email]",
            "MSprotectops3[SQ02]": "MSprotectops3[vpn]",
            "MSprotectops3[SQ03]": "MSprotectops3[tor]",
            "MSprotectops3[SQ04]": "MSprotectops3[e2e_chat]",
            "MSprotectops3[SQ05]": "MSprotectops3[encrypted_hardware]",
            "MSprotectops3[SQ06]": "MSprotectops3[2fa]",
            "MSprotectops3[SQ08]": "MSprotectops3[other]",
            "MSprotectleg3[SQ01]": "MSprotectleg3[free_counsel]",
            "MSprotectleg3[SQ02]": "MSprotectleg3[cost_insurance]",
            "MSprotectleg3[SQ03]": "MSprotectleg3[other]",
            "MSconstraintinter4[SQ01]": "MSconstraintinter4[police_search]",
            "MSconstraintinter4[SQ02]": "MSconstraintinter4[seizure]",
            "MSconstraintinter4[SQ03]": "MSconstraintinter4[extortion]",
            "MSconstraintinter4[SQ04]": "MSconstraintinter4[violent_threat]",
            "MSconstraintinter4[SQ05]": "MSconstraintinter4[inspection_during_travel]",
            "MSconstraintinter4[SQ06]": "MSconstraintinter4[detention]",
            "MSconstraintinter4[SQ07]": "MSconstraintinter4[surveillance_signalling]",
            "MSconstraintinter4[SQ08]": "MSconstraintinter4[online_harassment]",
            "MSconstraintinter4[SQ09]": "MSconstraintinter4[entry_on_deny_lists]",
            "MSconstraintinter4[SQ10]": "MSconstraintinter4[exclusion_from_events]",
            "MSconstraintinter4[SQ11]": "MSconstraintinter4[public_defamation]",
            "MSconstraintinter5[SQ01]": "MSconstraintinter5[unsolicited_information]",
            "MSconstraintinter5[SQ02]": "MSconstraintinter5[invitations]",
            "MSconstraintinter5[SQ03]": "MSconstraintinter5[other]",
            "MSconstraintinter6[SQ01]": "MSconstraintinter6[gender]",
            "MSconstraintinter6[SQ02]": "MSconstraintinter6[ethnicity]",
            "MSconstraintinter6[SQ03]": "MSconstraintinter6[political]",
            "MSconstraintinter6[SQ04]": "MSconstraintinter6[sexual]",
            "MSconstraintinter6[SQ05]": "MSconstraintinter6[religious]",
            "MSconstraintinter6[SQ06]": "MSconstraintinter6[other]",
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
            "MSprotectops1[sectraining]",
            "MSprotectops1[e2e]",
            "MSprotectops2",
            "MSprotectops3[encrypted_email]",
            "MSprotectops3[vpn]",
            "MSprotectops3[tor]",
            "MSprotectops3[e2e_chat]",
            "MSprotectops3[encrypted_hardware]",
            "MSprotectops3[2fa]",
            "MSprotectops3[other]",
            "MSprotectops4",
            "MSprotectleg1",
            "MSprotectleg2",
            "MSprotectleg3[free_counsel]",
            "MSprotectleg3[cost_insurance]",
            "MSprotectleg3[other]",
            "MSconstraintinter1",
            "MSconstraintinter2",
            "MSconstraintinter3",
            "MSconstraintinter4[police_search]",
            "MSconstraintinter4[seizure]",
            "MSconstraintinter4[extortion]",
            "MSconstraintinter4[violent_threat]",
            "MSconstraintinter4[inspection_during_travel]",
            "MSconstraintinter4[detention]",
            "MSconstraintinter4[surveillance_signalling]",
            "MSconstraintinter4[online_harassment]",
            "MSconstraintinter4[entry_on_deny_lists]",
            "MSconstraintinter4[exclusion_from_events]",
            "MSconstraintinter4[public_defamation]",
            "MSconstraintinter5[unsolicited_information]",
            "MSconstraintinter5[invitations]",
            "MSconstraintinter5[other]",
            "MSconstraintinter6[gender]",
            "MSconstraintinter6[ethnicity]",
            "MSconstraintinter6[political]",
            "MSconstraintinter6[sexual]",
            "MSconstraintinter6[religious]",
            "MSconstraintinter6[other]",
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
# Helper variables needed when answers are coded differently in the respective
# survey types
is_civsoc = df.surveytype == "Civil Society Scrutiny"
is_not_civsoc = df.surveytype == "Media Scrutiny"

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

df.loc[is_civsoc, "foi4"] = df["foi4"].replace(
    {
        "AO01": "Very helpful",
        "AO03": "Helpful in parts",
        "AO05": "Not helpful at all",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df.loc[is_not_civsoc, "foi4"] = df["foi4"].replace(
    {
        "AO01": "Very helpful",
        "AO02": "Helpful in parts",
        "AO03": "Not helpful at all",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["protectops1[sectraining]"] = df["protectops1[sectraining]"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

df["protectops1[e2e]"] = df["protectops1[e2e]"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

df["protectops2"] = df["protectops2"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

for label in [
    "encrypted_email",
    "vpn",
    "tor",
    "e2e_chat",
    "encrypted_hardware",
    "2fa",
    "other",
]:
    df[f"protectops3[{label}]"] = df[f"protectops3[{label}]"].replace(
        {
            "AO01": "Very important",
            "AO02": "Important",
            "AO03": "Somewhat important",
            "AO04": "Slightly important",
            "AO05": "Not important at all",
            "AO06": "I don't know",
            "AO07": "I prefer not to say",
        }
    )

df["protectops4"] = df["protectops4"].replace(
    {
        "AO01": "I have full confidence that the right tools will protect my communication from surveillance",
        "AO02": "Technological tools help to protect my identity to some extent, but an attacker with sufficient power may eventually be able to bypass my technological safeguards",
        "AO03": "Under the current conditions of communications surveillance, technological solutions cannot offer sufficient protection for the data I handle",
        "AO04": "I have no confidence in the protection offered by technological tools",
        "AO05": "I try to avoid technology-based communication whenever possible when I work on intelligence-related issues",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["protectleg1"] = df["protectleg1"].replace(
    {
        "AO01": "Always",
        "AO02": "Often",
        "AO03": "Sometimes",
        "AO04": "Rarely",
        "AO05": "Never",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["protectleg2"] = df["protectleg2"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

for label in ["free_counsel", "cost_insurance", "other"]:
    df[f"protectleg3[{label}]"] = df[f"protectleg3[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

df["constraintinter1"] = df["constraintinter1"].replace(
    {
        "AO01": "Yes, I have evidence",
        "AO02": "Yes, I suspect",
        "AO03": "No",
        "AO04": "I don't know",
        "AO05": "I prefer not to say",
    }
)

df["constraintinter2"] = df["constraintinter2"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

df["constraintinter3"] = df["constraintinter3"].replace(
    {
        "AO01": "I was threatened with prosecution",
        "AO02": "I was prosecuted but acquitted",
        "AO03": "I was prosecuted and convicted",
        "AO04": "I don't know",
        "AO05": "I prefer not to say",
    }
)

constraintinter4_options = [
    "police_search",
    "seizure",
    "extortion",
    "violent_threat",
    "inspection_during_travel",
    "detention",
    "surveillance_signalling",
    "online_harassment",
    "entry_on_deny_lists",
    "exclusion_from_events",
    "public_defamation",
]

for label in constraintinter4_options:
    df[f"constraintinter4[{label}]"] = df[f"constraintinter4[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

for label in ["unsolicited_information", "invitations", "other"]:
    df[f"constraintinter5[{label}]"] = df[f"constraintinter5[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

for label in ["gender", "ethnicity", "political", "sexual", "religious", "other"]:
    df[f"constraintinter6[{label}]"] = df[f"constraintinter6[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

df["attitude1"] = df["attitude1"].replace(
    {
        "AO01": "Intelligence agencies are incompatible with democratic <br>values and should be abolished",
        "AO02": "Intelligence agencies contradict democratic principles,<br>and their powers should be kept at a bare minimum",
        "AO03": "Intelligence agencies are necessary and legitimate institutions <br>of democratic states, even though they may sometimes overstep <br> their legal mandates",
        "AO04": "Intelligence agencies are a vital component of national <br>security and should be shielded from excessive bureaucratic <br> restrictions",
        "AO05": "I prefer not to say",
    }
)

df["attitude2"] = df["attitude2"].replace(
    {
        "AO01": "Intelligence oversight generally succeeds in uncovering <br>past misconduct and preventing future misconduct",
        "AO02": "Intelligence oversight is mostly effective, however its <br>institutional design needs reform for oversight practitioners to reliably <br>uncover past misconduct and prevent future misconduct",
        "AO03": "Intelligence oversight lacks efficacy, hence a fundamental <br>reorganization of oversight capacity is needed for oversight practitioners <br>to reliably uncover past misconduct and prevent future misconduct",
        "AO04": "Effective intelligence oversight is a hopeless endeavour <br>and even a systematic reorganization is unlikely to ensure <br>misconduct is uncovered and prevented.",
        "AO05": "I prefer not to say",
    }
)
###################################################################################
# Make answers analysable
###################################################################################
df["hr2"] = df["hr2"].replace("?", np.nan)
df["hr2"] = df["hr2"].replace("0,5", 0.5)
df["hr2"] = pd.to_numeric(df["hr2"], errors="coerce")

df["expertise1"] = df["expertise1"].replace("?", np.nan)
df["expertise1"] = df["expertise1"].replace("<1", 0.5)
df["expertise1"] = pd.to_numeric(df["expertise1"], errors="coerce")

df["foi2"] = df["foi2"].replace({"20+": 20.0, " ca 10": 10.0, "15+": 15.0})
df["foi2"] = pd.to_numeric(df["foi2"], errors="coerce")

# Save a useful snapshot of the merged data
df.to_pickle("./data/all.pkl")
df.to_excel("./data/all.xlsx")

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
    nbins=20,
    labels={"expertise1": "years"},
    color="country",
)
st.plotly_chart(expertise1_fig)

# Pie chart (expertise2)
st.write(
    "How do you assess your level of expertise concerning the **legal** aspects of surveillance by intelligence agencies? For example, knowledge of intelligence law, case law. `[expertise2]`"
)
expertise2_counts = df[filter]["expertise2"].value_counts()
expertise2_fig = px.pie(
    df[filter],
    values=expertise2_counts,
    names=expertise2_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
st.plotly_chart(expertise2_fig)

# Pie chart (expertise3)
st.write(
    "How do you assess your level of expertise concerning the **political** aspects of surveillance by intelligence agencies?` [expertise3]`"
)
expertise3_counts = df[filter]["expertise3"].value_counts()
expertise3_fig = px.pie(
    df[filter],
    values=expertise3_counts,
    names=expertise3_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
st.plotly_chart(expertise3_fig)

# Pie chart (expertise4)
st.write(
    "How do you assess your level of expertise concerning the **technical** aspects of surveillance by intelligence agencies?` [expertise4]`"
)
expertise4_counts = df[filter]["expertise4"].value_counts()
expertise4_fig = px.pie(
    df[filter],
    values=expertise4_counts,
    names=expertise4_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
st.plotly_chart(expertise4_fig)

# Pie Chart (finance1)
st.write(
    "How do you assess the financial resources that have been available for your work on intelligence over the past 5 years? `[finance1]`"
)
finance1_counts = df[filter]["finance1"].value_counts()
finance1_fig = px.pie(
    df[filter],
    values=finance1_counts,
    names=finance1_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
st.plotly_chart(finance1_fig)

# Pie Chart (foi1)
st.write(
    "Have you requested information under the national Freedom of Information Law  when you worked on intelligence-related issues over the past 5 years? `[foi1]`"
)
foi1_counts = df[filter]["foi1"].value_counts()
foi1_fig = px.pie(
    df[filter],
    values=foi1_counts,
    names=foi1_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
st.plotly_chart(foi1_fig)

# Histogram (foi2)
st.write("How often did you request information? `[foi2]`")
foi2_fig = px.histogram(
    df[filter],
    x="foi2",
    nbins=10,
    labels={"foi2": "Number of requests"},
    color="country",
)
st.plotly_chart(foi2_fig)

# Pie Chart (foi3)
st.write(
    "Over the past 5 years, did you receive a response to your FOI request(s) in a timely manner? `[foi3]`"
)
foi3_counts = df[filter]["foi3"].value_counts()
foi3_fig = px.pie(
    df[filter],
    values=foi3_counts,
    names=foi3_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
st.plotly_chart(foi3_fig)

# Pie Chart (foi4)
st.write(
    "How helpful have Freedom of Information requests been for your work on intelligence-related issues? `[foi4]`"
)
protectops2_counts = df[filter]["foi4"].value_counts()
protectops2_fig = px.pie(
    df[filter],
    values=protectops2_counts,
    names=protectops2_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
st.plotly_chart(protectops2_fig)

# Stacked Bar Chart (msprotectops1)
st.write(
    "Have you taken any of the following measures to protect your datas from attacks and surveillance? `[protectops1]`"
)
protectops1_options = [
    "Participation in digital security training",
    "Use of E2E encrypted communication channels",
]

protectops1_yes = []
protectops1_no = []
protectops1_dont_know = []
protectops1_prefer_not_to_say = []
for answer in [
    "Yes",
    "No",
    "I don't know",
    "I prefer not to say",
]:
    for label in ["sectraining", "e2e"]:
        try:
            count = df[filter][f"protectops1[{label}]"].value_counts()[answer]
        except KeyError:
            count = 0
        if answer == "Yes":
            protectops1_yes.append(count)
        elif answer == "No":
            protectops1_no.append(count)
        elif answer == "I don't know":
            protectops1_dont_know.append(count)
        elif answer == "I prefer not to say":
            protectops1_prefer_not_to_say.append(count)
        else:
            continue

protectops1_fig = go.Figure(
    data=[
        go.Bar(name="Yes", x=protectops1_options, y=protectops1_yes),
        go.Bar(name="No", x=protectops1_options, y=protectops1_no),
        go.Bar(name="I don't know", x=protectops1_options, y=protectops1_dont_know),
        go.Bar(
            name="I prefer not to say",
            x=protectops1_options,
            y=protectops1_prefer_not_to_say,
        ),
    ],
)

protectops1_fig.update_layout(
    width=800,
    height=800,
    barmode="stack",
)

st.plotly_chart(protectops1_fig)

# Pie chart (protectops2)
st.write("Were any of these measures provided by your employer? `[protectops2]`")
protectops2_counts = df[filter]["protectops2"].value_counts()
protectops2_fig = px.pie(
    df[filter],
    values=protectops2_counts,
    names=protectops2_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
st.plotly_chart(protectops2_fig)

# Stacked bar chart (protectops3)
st.write(
    "How important is the use of the following technical tools for you to protect your communications, your online activities and the data you handle? `[protectops3]`"
)
protectops3_options = [
    "Encrypted Email",
    "VPN",
    "Tor",
    "E2E Messengers",
    "Encrpyted hardware",
    "Two-Factor authentication",
    "Other",
]

protectops3_very_important = []
protectops3_somewhat_important = []
protectops3_important = []
protectops3_slightly_important = []
protectops3_not_important = []
for importance in [
    "Very important",
    "Somewhat important",
    "Important",
    "Slightly important",
    "Not important at all",
]:
    for label in [
        "encrypted_email",
        "vpn",
        "tor",
        "e2e_chat",
        "encrypted_hardware",
        "2fa",
        "other",
    ]:
        try:
            count = df[filter][f"protectops3[{label}]"].value_counts()[importance]
        except KeyError:
            count = 0
        if importance == "Very important":
            protectops3_very_important.append(count)
        elif importance == "Somewhat important":
            protectops3_somewhat_important.append(count)
        elif importance == "Important":
            protectops3_important.append(count)
        elif importance == "Slightly important":
            protectops3_slightly_important.append(count)
        elif importance == "Not important at all":
            protectops3_not_important.append(count)
        else:
            continue

protectops3_fig = go.Figure(
    data=[
        go.Bar(
            name="Very important",
            x=protectops3_options,
            y=protectops3_very_important,
            marker_color="#581845",
        ),
        go.Bar(
            name="Somewhat important",
            x=protectops3_options,
            y=protectops3_somewhat_important,
            marker_color="#900C3F",
        ),
        go.Bar(
            name="Important",
            x=protectops3_options,
            y=protectops3_important,
            marker_color="#C70039",
        ),
        go.Bar(
            name="Slightly important",
            x=protectops3_options,
            y=protectops3_slightly_important,
            marker_color="#FF5733",
        ),
        go.Bar(
            name="Not important at all",
            x=protectops3_options,
            y=protectops3_not_important,
            marker_color="#FFC300",
        ),
    ],
)

protectops3_fig.update_layout(width=800, height=800, barmode="stack")

st.plotly_chart(protectops3_fig)

# Pie chart (protectops4)
st.write(
    "Which of the following statements best describes your level of confidence in the protection offered by technological tools? `[protectops4]`"
)
protectops4_counts = df[filter]["protectops4"].value_counts()
protectops4_fig = px.pie(
    df[filter],
    values=protectops4_counts,
    names=protectops4_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)

st.plotly_chart(protectops4_fig, use_container_width=True)

# Pie chart (protectleg1)
st.write(
    "When working on intelligence-related issues, do you feel you have reason to be concerned about surveillance of your activities `[protectleg1]`"
)

protectleg1_counts = df[filter]["protectleg1"].value_counts()
protectleg1_fig = px.pie(
    df[filter],
    values=protectleg1_counts,
    names=protectleg1_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)

protectleg1_fig.update_layout(width=800, height=800)
st.plotly_chart(protectleg1_fig)

# Pie chart (protectleg2)
st.write(
    "Do you regard the existing legal protections against surveillance of your activities in your country as a sufficient safeguard for your work on intelligence-related issues? `[protectleg2]`"
)

protectleg2_counts = df[filter]["protectleg2"].value_counts()
protectleg2_fig = px.pie(
    df[filter],
    values=protectleg2_counts,
    names=protectleg2_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)

protectleg2_fig.update_layout(width=800, height=800)
st.plotly_chart(protectleg2_fig)

# Stacked bar chart (protectleg3)
st.write(
    "Are any of the following forms of institutional support readily available to you? `[protectleg3]`"
)
protectleg3_options = ["Free legal counsel", "Legal cost insurance", "Other"]
protectleg3_yes = []
protectleg3_no = []
protectleg3_dont_know = []
protectleg3_prefer_not_to_say = []
for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
    for label in ["free_counsel", "cost_insurance", "other"]:
        try:
            count = df[filter][f"protectleg3[{label}]"].value_counts()[answer]
        except KeyError:
            count = 0
        if answer == "Yes":
            protectleg3_yes.append(count)
        elif answer == "No":
            protectleg3_no.append(count)
        elif answer == "I don't know":
            protectleg3_dont_know.append(count)
        elif answer == "I prefer not to say":
            protectleg3_prefer_not_to_say.append(count)
        else:
            continue

protectleg3_fig = go.Figure(
    data=[
        go.Bar(
            name="Yes",
            x=protectleg3_options,
            y=protectleg3_yes,
            marker_color="#99c945",
        ),
        go.Bar(
            name="No",
            x=protectleg3_options,
            y=protectleg3_no,
            marker_color="#C70039",
        ),
        go.Bar(
            name="I don't know",
            x=protectleg3_options,
            y=protectleg3_dont_know,
            marker_color="#7f7f7f",
            opacity=0.8,
        ),
        go.Bar(
            name="I prefer not to say",
            x=protectleg3_options,
            y=protectleg3_prefer_not_to_say,
            marker_color="#525252",
            opacity=0.8,
        ),
    ],
)

protectleg3_fig.update_layout(width=800, height=800, barmode="stack")
st.plotly_chart(protectleg3_fig)

# Pie chart (constraintinter1)
st.write(
    "Has your institution or have you yourself been subjected to surveillance by intelligence agencies in the past five years? `[constraintinter1]`"
)

constraintinter1_counts = df[filter]["constraintinter1"].value_counts()
constraintinter1_fig = px.pie(
    df[filter],
    values=constraintinter1_counts,
    names=constraintinter1_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)

constraintinter1_fig.update_layout(width=800, height=800)
st.plotly_chart(constraintinter1_fig)

# Pie chart (constraintinter2)
st.write(
    "In the past 5 years, have you been threatened with prosecution or have you actually been prosecuted for your work on intelligence-related issues? `[constraintinter2]`"
)

constraintinter2_counts = df[filter]["constraintinter2"].value_counts()
constraintinter2_fig = px.pie(
    df[filter],
    values=constraintinter2_counts,
    names=constraintinter2_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)

constraintinter2_fig.update_layout(width=800, height=800)
st.plotly_chart(constraintinter2_fig)

# Pie chart (constraintinter3)
st.write("What was the outcome? `[constraintinter3]`")

constraintinter3_counts = df[filter]["constraintinter3"].value_counts()
constraintinter3_fig = px.pie(
    df[filter],
    values=constraintinter3_counts,
    names=constraintinter3_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)

constraintinter3_fig.update_layout(width=800, height=800)
st.plotly_chart(constraintinter3_fig)

# Stacked bar chart (constraintinter4)
st.write(
    "In the past 5 years, have you experienced any of the following interferences by public authorities in relation to your work on intelligence related topics? `[constraintinter4]`"
)
# TODO add proper labels
constraintinter4_yes = []
constraintinter4_no = []
constraintinter4_dont_know = []
constraintinter4_prefer_not_to_say = []
for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
    for label in constraintinter4_options:
        try:
            count = df[filter][f"constraintinter4[{label}]"].value_counts()[answer]
        except KeyError:
            count = 0
        if answer == "Yes":
            constraintinter4_yes.append(count)
        elif answer == "No":
            constraintinter4_no.append(count)
        elif answer == "I don't know":
            constraintinter4_dont_know.append(count)
        elif answer == "I prefer not to say":
            constraintinter4_prefer_not_to_say.append(count)
        else:
            continue

constraintinter4_fig = go.Figure(
    data=[
        go.Bar(
            name="Yes",
            x=constraintinter4_options,
            y=constraintinter4_yes,
            marker_color="#99c945",
        ),
        go.Bar(
            name="No",
            x=constraintinter4_options,
            y=constraintinter4_no,
            marker_color="#C70039",
        ),
        go.Bar(
            name="I don't know",
            x=constraintinter4_options,
            y=constraintinter4_dont_know,
            marker_color="#7f7f7f",
            opacity=0.8,
        ),
        go.Bar(
            name="I prefer not to say",
            x=constraintinter4_options,
            y=constraintinter4_prefer_not_to_say,
            marker_color="#525252",
            opacity=0.8,
        ),
    ],
)

constraintinter4_fig.update_layout(width=800, height=800, barmode="stack")
st.plotly_chart(constraintinter4_fig)

# Stacked bar chart (constraintinter5)
st.write(
    "In the past 5 years, have you been approached by intelligence officials and received... `[constraintinter5]`"
)
constraintinter5_options = [
    "Unsolicited information",
    "Invitations to off-the-record events or meetings",
    "Other",
]
constraintinter5_yes = []
constraintinter5_no = []
constraintinter5_dont_know = []
constraintinter5_prefer_not_to_say = []
for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
    for label in ["unsolicited_information", "invitations", "other"]:
        try:
            count = df[filter][f"constraintinter5[{label}]"].value_counts()[answer]
        except KeyError:
            count = 0
        if answer == "Yes":
            constraintinter5_yes.append(count)
        elif answer == "No":
            constraintinter5_no.append(count)
        elif answer == "I don't know":
            constraintinter5_dont_know.append(count)
        elif answer == "I prefer not to say":
            constraintinter5_prefer_not_to_say.append(count)
        else:
            continue

constraintinter5_fig = go.Figure(
    data=[
        go.Bar(
            name="Yes",
            x=constraintinter5_options,
            y=constraintinter5_yes,
            marker_color="#99c945",
        ),
        go.Bar(
            name="No",
            x=constraintinter5_options,
            y=constraintinter5_no,
            marker_color="#C70039",
        ),
        go.Bar(
            name="I don't know",
            x=constraintinter5_options,
            y=constraintinter5_dont_know,
            marker_color="#7f7f7f",
            opacity=0.8,
        ),
        go.Bar(
            name="I prefer not to say",
            x=constraintinter5_options,
            y=constraintinter5_prefer_not_to_say,
            marker_color="#525252",
            opacity=0.8,
        ),
    ],
)

constraintinter5_fig.update_layout(width=800, height=800, barmode="stack")
st.plotly_chart(constraintinter5_fig)

# Stacked bar chart (constraintinter6)
st.write(
    "When working on intelligence-related issues have you ever experienced harassment by security agencies or politicians due to your... `[constraintinter6]`"
)
constraintinter6_options = [
    "Gender",
    "Ethnicity",
    "Political orientation",
    "Sexual orientation",
    "Religious affiliation",
    "Other",
]
constraintinter6_yes = []
constraintinter6_no = []
constraintinter6_dont_know = []
constraintinter6_prefer_not_to_say = []
for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
    for label in ["gender", "ethnicity", "political", "sexual", "religious", "other"]:
        try:
            count = df[filter][f"constraintinter6[{label}]"].value_counts()[answer]
        except KeyError:
            count = 0
        if answer == "Yes":
            constraintinter6_yes.append(count)
        elif answer == "No":
            constraintinter6_no.append(count)
        elif answer == "I don't know":
            constraintinter6_dont_know.append(count)
        elif answer == "I prefer not to say":
            constraintinter6_prefer_not_to_say.append(count)
        else:
            continue

constraintinter6_fig = go.Figure(
    data=[
        go.Bar(
            name="Yes",
            x=constraintinter6_options,
            y=constraintinter6_yes,
            marker_color="#99c945",
        ),
        go.Bar(
            name="No",
            x=constraintinter6_options,
            y=constraintinter6_no,
            marker_color="#C70039",
        ),
        go.Bar(
            name="I don't know",
            x=constraintinter6_options,
            y=constraintinter6_dont_know,
            marker_color="#7f7f7f",
            opacity=0.8,
        ),
        go.Bar(
            name="I prefer not to say",
            x=constraintinter6_options,
            y=constraintinter6_prefer_not_to_say,
            marker_color="#525252",
            opacity=0.8,
        ),
    ],
)

constraintinter6_fig.update_layout(width=800, height=800, barmode="stack")
st.plotly_chart(constraintinter6_fig)

# Pie chart attitudes (attitude1)
st.write(
    "The following four statements are about **intelligence agencies**. Please select the statement you most agree with, based on your national context. `[attitude1]`"
)

attitude1_counts = df[filter]["attitude1"].value_counts()
attitude1_fig = px.pie(
    df[filter],
    values=attitude1_counts,
    names=attitude1_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)

attitude1_fig.update_layout(height=800, width=800)
st.plotly_chart(attitude1_fig)

# Pie chart attitudes (attitude2)
st.write(
    "The following four statements are about **intelligence oversight**. Please select the statement you most agree with, based on your national context. `[attitude2]`"
)

attitude2_counts = df[filter]["attitude2"].value_counts()
attitude2_fig = px.pie(
    df[filter],
    values=attitude2_counts,
    names=attitude2_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid,
)

attitude2_fig.update_layout(height=800, width=800)
st.plotly_chart(attitude2_fig)

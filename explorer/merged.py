import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

from lib.figures import (
    generate_pie_chart,
    generate_histogram,
    generate_overlaid_histogram,
    generate_stacked_bar_chart,
    generate_ranking_plot,
)

from lib.download import (
    get_csv_download_link,
    get_excel_download_link,
)


###############################################################################
# Helper functions
###############################################################################


@st.cache
def render_pie_chart(
    df,
    values,
    names,
    labels=None,
    color=None,
    color_discrete_sequence=px.colors.qualitative.Prism,
    color_discrete_map=None,
    hover_name=None,
):
    return generate_pie_chart(
        df,
        values,
        names,
        hover_name,
        color,
        color_discrete_sequence,
        color_discrete_map,
        labels,
    )


@st.cache
def render_histogram(df, x, y, nbins, color, color_discrete_map, labels):
    return generate_histogram(df, x, y, nbins, color, color_discrete_map, labels)


@st.cache
def render_overlaid_histogram(traces):
    return generate_overlaid_histogram(traces)


@st.cache
def render_stacked_bar_chart(data):
    return generate_stacked_bar_chart(data)


@st.cache
def render_ranking_plot(input_col):
    return generate_ranking_plot(df[filter], input_col, bodies, scoring)


@st.cache
def read_markdown_file(file):
    return Path(file).read_text()


@st.cache
def get_corr_matrix(df):
    df = pd.read_pickle("./data/merged_corr.pkl")
    fig = px.imshow(df, zmin=0, zmax=1, color_continuous_scale="viridis", height=1300)
    return fig


@st.cache
def get_significance_matrix(df):
    df = pd.read_pickle("./data/merged_sig.pkl")
    fig = px.imshow(df, zmin=-5, zmax=5, color_continuous_scale="viridis", height=1300)
    return fig


###################################################################################
# General configuration
###################################################################################


st.set_page_config(
    page_title="IOI Survey Data Explorer (CS & MS)",
)


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
            "CSfoi5[SQ01]": "CSfoi5[not_aware]",
            "CSfoi5[SQ02]": "CSfoi5[not_covered]",
            "CSfoi5[SQ03]": "CSfoi5[too_expensive]",
            "CSfoi5[SQ04]": "CSfoi5[too_time_consuming]",
            "CSfoi5[SQ05]": "CSfoi5[afraid_of_data_destruction]",
            "CSfoi5[SQ06]": "CSfoi5[afraid_of_discrimination]",
            "CSfoi5[SQ07]": "CSfoi5[other]",
            "CSfoi5[SQ08]": "CSfoi5[dont_know]",
            "CSfoi5[SQ09]": "CSfoi5[prefer_not_to_say]",
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
            "CSattitude3[SQ01]": "CSattitude3[rule_of_law]",
            "CSattitude3[SQ02]": "CSattitude3[civil_liberties]",
            "CSattitude3[SQ03]": "CSattitude3[effectiveness_of_intel]",
            "CSattitude3[SQ04]": "CSattitude3[legitimacy_of_intel]",
            "CSattitude3[SQ05]": "CSattitude3[trust_in_intel]",
            "CSattitude3[SQ06]": "CSattitude3[critique_of_intel]",
            "CSattitude3[SQ08]": "CSattitude3[prefer_not_to_say]",
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
            "CSfoi5[not_aware]",
            "CSfoi5[not_covered]",
            "CSfoi5[too_expensive]",
            "CSfoi5[too_time_consuming]",
            "CSfoi5[afraid_of_data_destruction]",
            "CSfoi5[afraid_of_discrimination]",
            "CSfoi5[other]",
            "CSfoi5[dont_know]",
            "CSfoi5[prefer_not_to_say]",
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
            "CSattitude3[rule_of_law]",
            "CSattitude3[civil_liberties]",
            "CSattitude3[effectiveness_of_intel]",
            "CSattitude3[legitimacy_of_intel]",
            "CSattitude3[trust_in_intel]",
            "CSattitude3[critique_of_intel]",
            "CSattitude3[prefer_not_to_say]",
            "CSattitude4[1]",
            "CSattitude4[2]",
            "CSattitude4[3]",
            "CSattitude4[4]",
            "CSattitude4[5]",
            "CSattitude4[6]",
            "CSattitude5[1]",
            "CSattitude5[2]",
            "CSattitude5[3]",
            "CSattitude5[4]",
            "CSattitude5[5]",
            "CSattitude5[6]",
            "CSattitude6[1]",
            "CSattitude6[2]",
            "CSattitude6[3]",
            "CSattitude6[4]",
            "CSattitude6[5]",
            "CSattitude6[6]",
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
            "MSfoi5[SQ01]": "MSfoi5[not_aware]",
            "MSfoi5[SQ02]": "MSfoi5[not_covered]",
            "MSfoi5[SQ03]": "MSfoi5[too_expensive]",
            "MSfoi5[SQ04]": "MSfoi5[too_time_consuming]",
            "MSfoi5[SQ05]": "MSfoi5[afraid_of_data_destruction]",
            "MSfoi5[SQ06]": "MSfoi5[afraid_of_discrimination]",
            "MSfoi5[SQ07]": "MSfoi5[other]",
            "MSfoi5[SQ08]": "MSfoi5[dont_know]",
            "MSfoi5[SQ09]": "MSfoi5[prefer_not_to_say]",
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
            "MSattitude3[SQ01]": "MSattitude3[rule_of_law]",
            "MSattitude3[SQ02]": "MSattitude3[civil_liberties]",
            "MSattitude3[SQ03]": "MSattitude3[effectiveness_of_intel]",
            "MSattitude3[SQ04]": "MSattitude3[legitimacy_of_intel]",
            "MSattitude3[SQ05]": "MSattitude3[trust_in_intel]",
            "MSattitude3[SQ06]": "MSattitude3[critique_of_intel]",
            "MSattitude3[SQ07]": "MSattitude3[prefer_not_to_say]",
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
            "MSfoi5[not_aware]",
            "MSfoi5[not_covered]",
            "MSfoi5[too_expensive]",
            "MSfoi5[too_time_consuming]",
            "MSfoi5[afraid_of_data_destruction]",
            "MSfoi5[afraid_of_discrimination]",
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
            "MSattitude3[rule_of_law]",
            "MSattitude3[civil_liberties]",
            "MSattitude3[effectiveness_of_intel]",
            "MSattitude3[legitimacy_of_intel]",
            "MSattitude3[trust_in_intel]",
            "MSattitude3[critique_of_intel]",
            "MSattitude3[prefer_not_to_say]",
            "MSattitude4[1]",
            "MSattitude4[2]",
            "MSattitude4[3]",
            "MSattitude4[4]",
            "MSattitude4[5]",
            "MSattitude4[6]",
            "MSattitude5[1]",
            "MSattitude5[2]",
            "MSattitude5[3]",
            "MSattitude5[4]",
            "MSattitude5[5]",
            "MSattitude5[6]",
            "MSattitude6[1]",
            "MSattitude6[2]",
            "MSattitude6[3]",
            "MSattitude6[4]",
            "MSattitude6[5]",
            "MSattitude6[6]",
        ]
    ]

    # Make column names compatible
    df.columns = df.columns.str[2:]

    # Set surveytype
    df["surveytype"] = "Media Scrutiny"
    return df


###############################################################################
# Define base DataFrame (Merge CS with MS)
###############################################################################


df_cs = get_merged_cs_df()
df_ms = get_merged_ms_df()
df = pd.concat([df_cs, df_ms], ignore_index=True)


###############################################################################
# Make answers human-readable
###############################################################################


# Helper variables needed when answers are coded differently in the respective
# survey types or languages
is_civsoc = df.surveytype == "Civil Society Scrutiny"
is_media = df.surveytype == "Media Scrutiny"
is_de = df.country == "Germany"
is_uk = df.country == "United Kingdom"
is_fr = df.country == "France"

df.loc[is_civsoc, "hr1"] = df["hr1"].replace(
    {
        "AO01": "Full-time",
        "AO02": "Part-time (>50%)",
        "AO03": "Part-time (<50%)",
        "AO04": "Freelance",
        "AO05": "Unpaid",
        "AO06": "Other",
        "AO07": "I don't know",
        "AO08": "I prefer not to say",
    }
)
df.loc[is_media, "hr1"] = df["hr1"].replace(
    {
        "AO01": "Full-time",
        "AO02": "Part-time (>50%)",
        "AO03": "Part-time (<50%)",
        "AO04": "Freelance",
        "AO05": "Unpaid",
        "AO08": "Other",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
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

df.loc[is_media, "foi4"] = df["foi4"].replace(
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

protectops3_options = [
    "encrypted_email",
    "vpn",
    "tor",
    "e2e_chat",
    "encrypted_hardware",
    "2fa",
    "other",
]
for label in protectops3_options:
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
# this was hard to spot. Only the CS survey for DE was coded as below
for label in protectops3_options:
    df.loc[(is_civsoc) & (is_de), f"protectops3[{label}]"] = df[
        f"protectops3[{label}]"
    ].replace(
        {
            "AO01": "Very important",
            "AO02": "Important",
            "AO03": "Somewhat important",
            "AO04": "Slightly important",
            "AO05": "Not important at all",
            # notice the AO09 instead of AO06 as above
            "AO09": "I don't know",
            "AO11": "I prefer not to say",
        }
    )

df["protectops4"] = df["protectops4"].replace(
    {
        "AO01": "I have full confidence that the right tools <br>will protect my communication from surveillance",
        "AO02": "Technological tools help to protect my identity <br>to some extent, but an attacker with sufficient power <br>may eventually be able to bypass my technological <br>safeguards",
        "AO03": "Under the current conditions of communications <br>surveillance, technological solutions cannot offer <br>sufficient protection for the data I handle",
        "AO04": "I have no confidence in the protection offered by <br>technological tools",
        "AO05": "I try to avoid technology-based communication whenever <br>possible when I work on intelligence-related issues",
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
        "AO03": "Intelligence agencies are necessary and legitimate institutions <br>of democratic states, even though they may sometimes overstep <br>their legal mandates",
        "AO04": "Intelligence agencies are a vital component of national <br>security and should be shielded from excessive bureaucratic <br>restrictions",
        "AO05": "I prefer not to say",
    }
)

df["attitude2"] = df["attitude2"].replace(
    {
        "AO01": "Intelligence oversight generally succeeds in uncovering <br>past misconduct and preventing future misconduct",
        "AO02": "Intelligence oversight is mostly effective, however its <br>institutional design needs reform for oversight practitioners <br> to reliably uncover past misconduct and prevent future <br>misconduct",
        "AO03": "Intelligence oversight lacks efficacy, hence a fundamental <br>reorganization of oversight capacity is needed for oversight <br>practitioners to reliably uncover past misconduct and <br>prevent future misconduct",
        "AO04": "Effective intelligence oversight is a hopeless endeavour <br>and even a systematic reorganization is unlikely to ensure <br>misconduct is uncovered and prevented.",
        "AO05": "I prefer not to say",
    }
)

for i in range(4, 7):
    for j in range(1, 7):
        df[f"attitude{i}[{j}]"] = df[f"attitude{i}[{j}]"].replace(
            {
                "AO01": "Parliamentary oversight bodies",
                "AO02": "Judicial oversight bodies",
                "AO03": "Independent expert bodies",
                "AO04": "Data protection authorities",
                "AO05": "Audit courts",
                "AO06": "CSOs | The media",
            }
        )
        # Here, CS FR is coded differently
        df.loc[(is_fr) & (is_civsoc), f"attitude{i}[{j}]"] = df[
            f"attitude{i}[{j}]"
        ].replace(
            {
                "AO01": "Parliamentary oversight bodies",
                "AO02": "Judicial oversight bodies",
                "AO03": "Independent expert bodies",
                "AO04": "Data protection authorities",
                "AO07": "Audit courts",
                "AO06": "CSOs | The media",
            }
        )

###############################################################################
# Make answers analysable (change data types etc.)
###############################################################################


df["hr2"] = df["hr2"].replace("?", np.nan)
df["hr2"] = df["hr2"].replace("0,5", 0.5)
df["hr2"] = pd.to_numeric(df["hr2"], errors="coerce")

df["expertise1"] = df["expertise1"].replace("?", np.nan)
df["expertise1"] = df["expertise1"].replace("<1", 0.5)
df["expertise1"] = pd.to_numeric(df["expertise1"], errors="coerce")

df["foi2"] = df["foi2"].replace(
    {"20+": 20.0, " ca 10": 10.0, "several": 3.0, "15+": 15.0}
)
df["foi2"] = pd.to_numeric(df["foi2"], errors="coerce")

# Here, I change the datatype to boolean for all the multiple choice answers
for col in df:
    if col.startswith("foi5") or col.startswith("attitude3"):
        df[col] = df[col].replace(np.nan, False)
        df[col] = df[col].replace("Y", True)
        df[col] = df[col].astype("bool")


###############################################################################
# Filter logic
###############################################################################


filters = {
    "surveytype": st.sidebar.selectbox(
        "Survey type", ["All", "Civil Society Scrutiny", "Media Scrutiny"]
    ),
    "country": st.sidebar.selectbox(
        "Country", ["All", "United Kingdom", "Germany", "France"]
    ),
}

filter = np.full(len(df.index), True)
for column_name, selectbox in filters.items():
    if selectbox == "All":
        continue
    else:
        filter = filter & (df[column_name] == selectbox)


###############################################################################
# Save a useful snapshot of the merged data (comment out for production)
###############################################################################


# df.to_pickle("./data/merged.pkl")
# df.to_excel("./data/merged.xlsx")
# df.to_csv("./data/merged.csv")


###############################################################################
# Custom CSS
###############################################################################


st.markdown(
    """ <style> h3 {line-height: 1.3} </style> """,
    unsafe_allow_html=True,
)


###############################################################################
# Display dynamic charts
###############################################################################


st.title("IOI Survey Data Explorer (CS & MS)")

st.write("# General")

merged_markdown = read_markdown_file("explorer/markdown/merged.md")
st.markdown(merged_markdown, unsafe_allow_html=True)

st.write("### Country `[country]`")
country_counts = df[filter]["country"].value_counts()
st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=country_counts,
        names=country_counts.index,
    )
)

st.write("### Surveytype `[surveytype]`")
surveytype_counts = df[filter]["surveytype"].value_counts()
st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=surveytype_counts,
        names=surveytype_counts.index,
    )
)

st.write("# Resources")

st.write("## Human Resources")

st.write("### What is your employment status `[hr1]`")
hr1_counts = df[filter]["hr1"].value_counts()
st.plotly_chart(
    render_pie_chart(
        hr1_counts,
        values=hr1_counts,
        names=hr1_counts.index,
        color=hr1_counts.index,
        color_discrete_map={
            "Full-time": px.colors.qualitative.Prism[0],
            "Part-time (>50%)": px.colors.qualitative.Prism[1],
            "Part-time (<50%)": px.colors.qualitative.Prism[2],
            "Freelance": px.colors.qualitative.Prism[4],
            "Other": px.colors.qualitative.Prism[10],
        },
    )
)

st.write(
    "### How many days per month do you work on surveillance by intelligence agencies? `[hr2]`"
)
st.plotly_chart(
    render_histogram(
        df=df[filter],
        x="hr2",
        y=None,
        nbins=None,
        color="country",
        color_discrete_map={
            "Germany": px.colors.qualitative.Prism[5],
            "France": px.colors.qualitative.Prism[1],
            "United Kingdom": px.colors.qualitative.Prism[7],
        },
        labels={"hr2": "days per month"},
    )
)

# st.write(
#     "### Who works more than 5 days on surveillance by intelligence agencies? `[hr2]`"
# )
# df["hr2_more_than_five"] = np.where(df[filter]["hr2"] > 5, True, False)
# hr2_more_than_five_counts = df[filter]["hr2_more_than_five"].value_counts()
# st.plotly_chart(
#     render_pie_chart(
#         hr2_more_than_five_counts,
#         values=hr2_more_than_five_counts,
#         names=hr2_more_than_five_counts.index,
#         color=hr2_more_than_five_counts.index,
#         labels={"true": ">5 days", "false": "<5 days"},
#     )
# )


st.write("## Expertise")

# TODO Show distribution/average for the three countries
st.write(
    "### How many years have you spent working on surveillance by intelligence agencies? `[expertise1]`"
)
st.plotly_chart(
    render_histogram(
        df[filter],
        x="expertise1",
        y=None,
        nbins=20,
        color="country",
        color_discrete_map={
            "Germany": px.colors.qualitative.Prism[5],
            "France": px.colors.qualitative.Prism[1],
            "United Kingdom": px.colors.qualitative.Prism[7],
        },
        labels={"expertise1": "years"},
    )
)

st.write(
    "### How do you assess your level of expertise concerning the **legal** aspects of surveillance by intelligence agencies? For example, knowledge of intelligence law, case law. `[expertise2]`"
)
expertise2_counts = df[filter]["expertise2"].value_counts()
st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=expertise2_counts,
        names=expertise2_counts.index,
        color_discrete_sequence=None,
        color=expertise2_counts.index,
        color_discrete_map={
            "Expert knowledge": px.colors.qualitative.Prism[9],
            "Advanced knowledge": px.colors.qualitative.Prism[8],
            "Some knowledge": px.colors.qualitative.Prism[7],
            "Basic knowledge": px.colors.qualitative.Prism[6],
            "No knowledge": px.colors.qualitative.Prism[5],
            "I don't know": px.colors.qualitative.Prism[10],
            "I prefer not to say": px.colors.qualitative.Prism[10],
        },
    )
)

st.write(
    "### How do you assess your level of expertise concerning the **political** aspects of surveillance by intelligence agencies?` [expertise3]`"
)
expertise3_counts = df[filter]["expertise3"].value_counts()
st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=expertise3_counts,
        names=expertise3_counts.index,
        color_discrete_sequence=None,
        color=expertise3_counts.index,
        color_discrete_map={
            "Expert knowledge": px.colors.qualitative.Prism[9],
            "Advanced knowledge": px.colors.qualitative.Prism[8],
            "Some knowledge": px.colors.qualitative.Prism[7],
            "Basic knowledge": px.colors.qualitative.Prism[6],
            "No knowledge": px.colors.qualitative.Prism[5],
            "I don't know": px.colors.qualitative.Prism[10],
            "I prefer not to say": px.colors.qualitative.Prism[10],
        },
    )
)

st.write(
    "### How do you assess your level of expertise concerning the **technical** aspects of surveillance by intelligence agencies?` [expertise4]`"
)
expertise4_counts = df[filter]["expertise4"].value_counts()
st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=expertise4_counts,
        names=expertise4_counts.index,
        color_discrete_sequence=None,
        color=expertise4_counts.index,
        color_discrete_map={
            "Expert knowledge": px.colors.qualitative.Prism[9],
            "Advanced knowledge": px.colors.qualitative.Prism[8],
            "Some knowledge": px.colors.qualitative.Prism[7],
            "Basic knowledge": px.colors.qualitative.Prism[6],
            "No knowledge": px.colors.qualitative.Prism[5],
            "I don't know": px.colors.qualitative.Prism[10],
            "I prefer not to say": px.colors.qualitative.Prism[10],
        },
    )
)

st.write("## Financial Resources")

st.write(
    "### How do you assess the financial resources that have been available for your work on intelligence over the past 5 years? `[finance1]`"
)
finance1_counts = df[filter]["finance1"].value_counts()
st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=finance1_counts,
        names=finance1_counts.index,
        color_discrete_sequence=None,
        color=finance1_counts.index,
        color_discrete_map={
            "A great deal of funding": px.colors.qualitative.Prism[9],
            "Sufficient funding": px.colors.qualitative.Prism[8],
            "Some funding": px.colors.qualitative.Prism[7],
            "Little funding": px.colors.qualitative.Prism[6],
            "No funding": px.colors.qualitative.Prism[5],
            "I don't know": px.colors.qualitative.Prism[10],
            "I prefer not to say": px.colors.qualitative.Prism[10],
        },
    )
)

st.write("## Freedom of Information")

st.write(
    "### Have you requested information under the national FOI law when you worked on intelligence-related issues over the past 5 years? `[foi1]`"
)
foi1_counts = df[filter]["foi1"].value_counts()
st.plotly_chart(
    render_pie_chart(
        foi1_counts,
        values=foi1_counts,
        names=foi1_counts.index,
        color=foi1_counts.index,
        color_discrete_map={
            "No": px.colors.qualitative.Prism[8],
            "Yes": px.colors.qualitative.Prism[2],
            "I don't know": px.colors.qualitative.Prism[10],
            "I prefer not to say": px.colors.qualitative.Prism[10],
        },
    )
)

st.write("### How often did you request information? `[foi2]`")
st.plotly_chart(
    render_histogram(
        df[filter],
        x="foi2",
        y=None,
        nbins=10,
        color="country",
        color_discrete_map={
            "Germany": px.colors.qualitative.Prism[5],
            "France": px.colors.qualitative.Prism[1],
            "United Kingdom": px.colors.qualitative.Prism[7],
        },
        labels={"foi2": "Number of requests"},
    )
)

st.write(
    "### Over the past 5 years, did you receive a response to your FOI request(s) in a timely manner? `[foi3]`"
)
foi3_counts = df[filter]["foi3"].value_counts()
st.plotly_chart(
    render_pie_chart(
        foi3_counts,
        values=foi3_counts,
        names=foi3_counts.index,
        color=foi3_counts.index,
        color_discrete_map={
            "Never": px.colors.qualitative.Prism[9],
            "No, usually longer than 30 days": px.colors.qualitative.Prism[8],
            "Yes, within 30 days": px.colors.qualitative.Prism[2],
            "I don't know": px.colors.qualitative.Prism[10],
            "I prefer not to say": px.colors.qualitative.Prism[10],
        },
    )
)

st.write(
    "### How helpful have Freedom of Information requests been for your work on intelligence-related issues? `[foi4]`"
)
protectops2_counts = df[filter]["foi4"].value_counts()

st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=protectops2_counts,
        names=protectops2_counts.index,
    )
)

st.write(
    "### Why haven’t you requested information under the national FOI law when you reported on intelligence-related issues over the past 5 years? `[foi5]`"
)
foi5_df = pd.DataFrame(columns=("option", "count", "country"))
# TODO Map proper labels
for label in [
    "not_aware",
    "not_covered",
    "too_expensive",
    "too_time_consuming",
    "afraid_of_data_destruction",
    "afraid_of_discrimination",
    "other",
    "dont_know",
    "prefer_not_to_say",
]:
    foi5_data = df[filter]["country"][df[f"foi5[{label}]"] == 1].tolist()
    for i in foi5_data:
        foi5_df = foi5_df.append(
            {"option": label, "count": foi5_data.count(i), "country": i},
            ignore_index=True,
        )
foi5_df = foi5_df.drop_duplicates()
st.plotly_chart(
    render_histogram(
        foi5_df,
        x="option",
        y="count",
        nbins=None,
        color="country",
        color_discrete_map={
            "Germany": px.colors.qualitative.Prism[5],
            "France": px.colors.qualitative.Prism[1],
            "United Kingdom": px.colors.qualitative.Prism[7],
        },
        labels={"count": "people who answered 'Yes'"},
    )
)

st.write("# Protection")

st.write("## Operational Protection")

st.write(
    "### Have you taken any of the following measures to protect your datas from attacks and surveillance? `[protectops1]`"
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

st.plotly_chart(
    generate_stacked_bar_chart(
        data=[
            go.Bar(
                name="Yes",
                x=protectops1_options,
                y=protectops1_yes,
                marker_color=px.colors.qualitative.Prism[2],
            ),
            go.Bar(
                name="No",
                x=protectops1_options,
                y=protectops1_no,
                marker_color=px.colors.qualitative.Prism[8],
            ),
            go.Bar(
                name="I don't know",
                x=protectops1_options,
                y=protectops1_dont_know,
                marker_color=px.colors.qualitative.Prism[10],
            ),
            go.Bar(
                name="I prefer not to say",
                x=protectops1_options,
                y=protectops1_prefer_not_to_say,
                marker_color=px.colors.qualitative.Prism[10],
            ),
        ],
    )
)

st.write("### Were any of these measures provided by your employer? `[protectops2]`")
protectops2_counts = df[filter]["protectops2"].value_counts()
st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=protectops2_counts,
        names=protectops2_counts.index,
        color_discrete_sequence=px.colors.qualitative.Prism,
    )
)

st.write(
    "### How important is the use of the following technical tools for you to protect your communications, your online activities and the data you handle? `[protectops3]`"
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

st.plotly_chart(
    generate_stacked_bar_chart(
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
)

st.write(
    "### Which of the following statements best describes your level of confidence in the protection offered by technological tools? `[protectops4]`"
)
protectops4_counts = df[filter]["protectops4"].value_counts()
st.plotly_chart(
    render_pie_chart(
        protectops4_counts,
        values=protectops4_counts,
        names=protectops4_counts.index,
        color=protectops4_counts.index,
        color_discrete_map={
            "I have full confidence that the right tools <br>will protect my communication from surveillance": px.colors.qualitative.Prism[
                4
            ],
            "Technological tools help to protect my identity <br>to some extent, but an attacker with sufficient power <br>may eventually be able to bypass my technological <br>safeguards": px.colors.qualitative.Prism[
                5
            ],
            "Under the current conditions of communications <br>surveillance, technological solutions cannot offer <br>sufficient protection for the data I handle": px.colors.qualitative.Prism[
                6
            ],
            "I have no confidence in the protection offered by <br>technological tools": px.colors.qualitative.Prism[
                7
            ],
            "I try to avoid technology-based communication whenever <br>possible when I work on intelligence-related issues": px.colors.qualitative.Prism[
                8
            ],
            "I don't know": px.colors.qualitative.Prism[10],
            "I prefer not to say": px.colors.qualitative.Prism[10],
        },
    )
)

st.write("## Legal Protection")

st.write(
    "### When working on intelligence-related issues, do you feel you have reason to be concerned about surveillance of your activities `[protectleg1]`"
)

protectleg1_counts = df[filter]["protectleg1"].value_counts()
st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=protectleg1_counts,
        names=protectleg1_counts.index,
        color=protectleg1_counts.index,
        color_discrete_map={
            "Always": px.colors.qualitative.Prism[9],
            "Often": px.colors.qualitative.Prism[8],
            "Sometimes": px.colors.qualitative.Prism[7],
            "Rarely": px.colors.qualitative.Prism[6],
            "Never": px.colors.qualitative.Prism[5],
            "I don't know": px.colors.qualitative.Prism[10],
            "I prefer not to say": px.colors.qualitative.Prism[10],
        },
    )
)

st.write(
    "### Do you regard the existing legal protections against surveillance of your activities in your country as a sufficient safeguard for your work on intelligence-related issues? `[protectleg2]`"
)

protectleg2_counts = df[filter]["protectleg2"].value_counts()
st.plotly_chart(
    render_pie_chart(
        protectleg2_counts,
        values=protectleg2_counts,
        names=protectleg2_counts.index,
        color_discrete_sequence=px.colors.qualitative.Prism,
        color=protectleg2_counts.index,
        color_discrete_map={
            "No": px.colors.qualitative.Prism[8],
            "Yes": px.colors.qualitative.Prism[2],
            "I don't know": px.colors.qualitative.Prism[10],
            "I prefer not to say": px.colors.qualitative.Prism[10],
        },
    )
)

st.write(
    "### Are any of the following forms of institutional support readily available to you? `[protectleg3]`"
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

st.plotly_chart(
    generate_stacked_bar_chart(
        data=[
            go.Bar(
                name="Yes",
                x=protectleg3_options,
                y=protectleg3_yes,
                marker_color=px.colors.qualitative.Prism[2],
            ),
            go.Bar(
                name="No",
                x=protectleg3_options,
                y=protectleg3_no,
                marker_color=px.colors.qualitative.Prism[8],
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
)

st.write("# Constraints")

st.write("## Interferences")

st.write(
    "### Has your institution or have you yourself been subjected to surveillance by intelligence agencies in the past five years? `[constraintinter1]`"
)

constraintinter1_counts = df[filter]["constraintinter1"].value_counts()
st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=constraintinter1_counts,
        names=constraintinter1_counts.index,
        color=constraintinter1_counts.index,
        color_discrete_map={
            "No": px.colors.qualitative.Prism[8],
            "Yes, I have evidence": px.colors.qualitative.Prism[1],
            "Yes, I suspect": px.colors.qualitative.Prism[2],
            "I don't know": px.colors.qualitative.Prism[10],
            "I prefer not to say": px.colors.qualitative.Prism[10],
        },
    )
)

st.write(
    "### In the past 5 years, have you been threatened with prosecution or have you actually been prosecuted for your work on intelligence-related issues? `[constraintinter2]`"
)

constraintinter2_counts = df[filter]["constraintinter2"].value_counts()
constraintinter2_fig = px.pie(
    df[filter],
    values=constraintinter2_counts,
    names=constraintinter2_counts.index,
    color_discrete_sequence=px.colors.qualitative.Prism,
)

st.plotly_chart(constraintinter2_fig)

st.write("### What was the outcome? `[constraintinter3]`")

constraintinter3_counts = df[filter]["constraintinter3"].value_counts()
st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=constraintinter3_counts,
        names=constraintinter3_counts.index,
        color_discrete_sequence=px.colors.qualitative.Prism,
    )
)

st.write(
    "### In the past 5 years, have you experienced any of the following interferences by public authorities in relation to your work on intelligence related topics? `[constraintinter4]`"
)
# TODO Map proper labels
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
st.plotly_chart(
    generate_stacked_bar_chart(
        data=[
            go.Bar(
                name="Yes",
                x=constraintinter4_options,
                y=constraintinter4_yes,
                marker_color=px.colors.qualitative.Prism[2],
            ),
            go.Bar(
                name="No",
                x=constraintinter4_options,
                y=constraintinter4_no,
                marker_color=px.colors.qualitative.Prism[8],
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
)

st.write(
    "### In the past 5 years, have you been approached by intelligence officials and received... `[constraintinter5]`"
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

st.plotly_chart(
    generate_stacked_bar_chart(
        data=[
            go.Bar(
                name="Yes",
                x=constraintinter5_options,
                y=constraintinter5_yes,
                marker_color=px.colors.qualitative.Prism[2],
            ),
            go.Bar(
                name="No",
                x=constraintinter5_options,
                y=constraintinter5_no,
                marker_color=px.colors.qualitative.Prism[8],
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
)

st.write(
    "### When working on intelligence-related issues have you ever experienced harassment by security agencies or politicians due to your... `[constraintinter6]`"
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

st.plotly_chart(
    generate_stacked_bar_chart(
        data=[
            go.Bar(
                name="Yes",
                x=constraintinter6_options,
                y=constraintinter6_yes,
                marker_color=px.colors.qualitative.Prism[2],
            ),
            go.Bar(
                name="No",
                x=constraintinter6_options,
                y=constraintinter6_no,
                marker_color=px.colors.qualitative.Prism[8],
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
)

st.write("# Attitude")

st.write(
    "### The following four statements are about **intelligence agencies**. Please select the statement you most agree with, based on your national context. `[attitude1]`"
)

attitude1_counts = df[filter]["attitude1"].value_counts()
st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=attitude1_counts,
        names=attitude1_counts.index,
        color_discrete_sequence=px.colors.qualitative.Prism,
    )
)

# Pie chart attitudes (attitude2)
st.write(
    "### The following four statements are about **intelligence oversight**. Please select the statement you most agree with, based on your national context. `[attitude2]`"
)

attitude2_counts = df[filter]["attitude2"].value_counts()
st.plotly_chart(
    render_pie_chart(
        df[filter],
        values=attitude2_counts,
        names=attitude2_counts.index,
        color_discrete_sequence=px.colors.qualitative.Prism,
    )
)

# Histogram (attitude3)

st.write(
    "### In your personal view, what are the goals of intelligence oversight? Please select the three goals of oversight you subscribe to the most. `[attitude3]`"
)

attitude3_options = [
    "rule_of_law",
    "civil_liberties",
    "effectiveness_of_intel",
    "legitimacy_of_intel",
    "trust_in_intel",
    "critique_of_intel",
    "prefer_not_to_say",
]

attitude3_df = pd.DataFrame(columns=("option", "count", "country"))
for label in attitude3_options:
    attitude3_data = df[filter]["country"][df[f"attitude3[{label}]"] == 1].tolist()
    for i in attitude3_data:
        attitude3_df = attitude3_df.append(
            {"option": label, "count": attitude3_data.count(i), "country": i},
            ignore_index=True,
        )
attitude3_df = attitude3_df.drop_duplicates()

st.plotly_chart(
    generate_histogram(
        df=attitude3_df,
        x="option",
        y="count",
        nbins=None,
        color="country",
        color_discrete_map={
            "Germany": px.colors.qualitative.Prism[5],
            "France": px.colors.qualitative.Prism[1],
            "United Kingdom": px.colors.qualitative.Prism[7],
        },
        labels={"count": "people who answered 'Yes'"},
    )
)


scoring = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}
bodies = [
    "Parliamentary oversight bodies",
    "Judicial oversight bodies",
    "Independent expert bodies",
    "Data protection authorities",
    "Audit courts",
    "CSOs | The media",
]

st.write(
    "### Which of the following actors do you trust the most to **enable public debate** on surveillance by intelligence agencies? `[attitude4]`"
)
st.plotly_chart(render_ranking_plot("attitude4"))

st.write(
    "### Which of the following actors do you trust the most to **contest surveillance** by intelligence agencies? `[attitude5]`"
)
st.plotly_chart(render_ranking_plot("attitude5"))

st.write(
    "### Which of the following actors do you trust the most to **enforce compliance** regarding surveillance by intelligence agencies? `[attitude6]`"
)
st.plotly_chart(render_ranking_plot("attitude6"))


###############################################################################
# Appendix
###############################################################################


st.write("# Appendix")

st.write("## Raw data")

st.write(get_csv_download_link(df, "merged"), unsafe_allow_html=True)
st.write(get_excel_download_link(df, "merged"), unsafe_allow_html=True)

table = st.checkbox("Show data as table")
if table:
    st.dataframe(df[filter])

st.write("## Correlation Matrix (Phik `φK`)")

st.write(
    "Phik (φk) is a new and practical correlation coefficient that works consistently between categorical, ordinal and interval variables, captures non-linear dependency and reverts to the Pearson correlation coefficient in case of a bivariate normal input distribution. There is extensive documentation available [here](https://phik.readthedocs.io/en/latest/index.html)"
)

show_corr = st.checkbox("Show correlation matrix")
if show_corr:
    fig_corr = get_corr_matrix(df)
    st.plotly_chart(fig_corr, use_container_width=True)

st.write("## Significance Matrix")

st.markdown(
    body="When assessing correlations it is good practise to evaluate both the correlation and the significance of the correlation: a large correlation may be statistically insignificant, and vice versa a small correlation may be very significant. For instance, scipy.stats.pearsonr returns both the pearson correlation and the p-value. Similarly, the phik package offers functionality the calculate a significance matrix. Significance is defined as: "
)
st.markdown(
    body="$Z=\Phi^{-1}(1-p); \Phi(z)=\\frac{1}{\\sqrt{2\pi}}\int_{-\infty}^{z} e^{-t^{2}/2}\,dt$"
)

show_sig = st.checkbox("Show significance matrix")
if show_sig:
    fig_sig = get_significance_matrix(df)
    st.plotly_chart(fig_sig, use_container_width=True)

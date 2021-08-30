import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

from lib.figures import (
    generate_pie_chart,
    generate_boxplot,
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
    color=None,
    color_discrete_sequence=px.colors.qualitative.Prism,
    hover_data=None,
    custom_data=None,
    color_discrete_map=None,
    hover_name=None,
    labels=None,
):
    return generate_pie_chart(
        df,
        values,
        names,
        hover_name,
        color,
        hover_data,
        custom_data,
        color_discrete_sequence,
        color_discrete_map,
        labels,
    )


@st.cache
def render_boxplot(df, x, y, color=None, points="all", color_discrete_map=None):
    return generate_boxplot(df, x, y, points, color, color_discrete_map)


@st.cache
def render_histogram(df, x, y, nbins, color, color_discrete_map, labels):
    return generate_histogram(df, x, y, nbins, color, color_discrete_map, labels)


@st.cache
def render_overlaid_histogram(traces, names, colors):
    return generate_overlaid_histogram(traces, names, colors)


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
    df = pd.read_pickle("./data/media_corr.pkl")
    fig = px.imshow(df, zmin=0, zmax=1, color_continuous_scale="viridis", height=1300)
    return fig


@st.cache
def get_significance_matrix(df):
    df = pd.read_pickle("./data/media_sig.pkl")
    fig = px.imshow(df, zmin=-5, zmax=5, color_continuous_scale="viridis", height=1300)
    return fig


###############################################################################
# General configuration
###############################################################################


st.set_page_config(
    page_title="IOI Survey Data Explorer | CSO",
)


###############################################################################
# Data wrangling
###############################################################################


@st.cache()
def get_cs_df():
    # Merge CSV files into DataFrame
    cs_csv_files = [
        "data/cs_uk_short.csv",
        "data/cs_de_short.csv",
        "data/cs_fr_short.csv",
    ]
    df_list = []
    for csv in cs_csv_files:
        df_list.append(pd.read_csv(csv, sep=";"))
    df = pd.concat(df_list, ignore_index=True)

    # Rename columns
    df = df.rename(
        columns={
            "startlanguage": "country",
            "lastpage": "lastpage",
            "CSfinance2[SQ01]": "CSfinance2[private_foundations]",
            "CSfinance2[SQ02]": "CSfinance2[donations]",
            "CSfinance2[SQ03]": "CSfinance2[national_public_funds]",
            "CSfinance2[SQ04]": "CSfinance2[corporate_sponsorship]",
            "CSfinance2[SQ05]": "CSfinance2[international_public_funds]",
            "CSfinance2[SQ06]": "CSfinance2[other]",
            "CSfoi5[SQ01]": "CSfoi5[not_aware]",
            "CSfoi5[SQ02]": "CSfoi5[not_covered]",
            "CSfoi5[SQ03]": "CSfoi5[too_expensive]",
            "CSfoi5[SQ04]": "CSfoi5[too_time_consuming]",
            "CSfoi5[SQ05]": "CSfoi5[afraid_of_data_destruction]",
            "CSfoi5[SQ06]": "CSfoi5[afraid_of_discrimination]",
            "CSfoi5[SQ07]": "CSfoi5[other]",
            "CSfoi5[SQ08]": "CSfoi5[dont_know]",
            "CSfoi5[SQ09]": "CSfoi5[prefer_not_to_say]",
            "CSfoi5specify": "CSfoi5other",
            "CScampact1[SQ01]": "CScampact1[1]",
            "CScampact1[SQ07]": "CScampact1[2]",
            "CScampact1[SQ03]": "CScampact1[3]",
            "CScampact1[SQ04]": "CScampact1[4]",
            "CScampact1[SQ05]": "CScampact1[5]",
            "CScampact1[SQ06]": "CScampact1[6]",
            "CScampact1[SQ08]": "CScampact1[7]",
            "CScampact1[SQ09]": "CScampact1[8]",
            "CScampact2[SQ01]": "CScampact2[media_contributions]",
            "CScampact2[SQ02]": "CScampact2[own_publications]",
            "CScampact2[SQ03]": "CScampact2[petitions_open_letters]",
            "CScampact2[SQ04]": "CScampact2[public_events]",
            "CScampact2[SQ05]": "CScampact2[collaborations]",
            "CScampact2[SQ06]": "CScampact2[demonstrations]",
            "CScampact2[SQ07]": "CScampact2[social_media]",
            "CScampact2[SQ08]": "CScampact2[advertising]",
            "CScampact2[SQ09]": "CScampact2[volunteer_activities]",
            "CScampact2[SQ10]": "CScampact2[providing_technical_tools]",
            "CScampact2[SQ11]": "CScampact2[support_for_eu_campaigns]",
            "CScampact2[SQ12]": "CScampact2[other]",
            "CScampimpact1[SQ01]": "CScampimpact1[increased_awareness]",
            "CScampimpact1[SQ02]": "CScampimpact1[policies_reflect_demands]",
            "CScampimpact1[SQ03]": "CScampimpact1[created_media_attention]",
            "CScampimpact1[SQ04]": "CScampimpact1[achieved_goals]",
            "CSadvocact1[SQ01]": "CSadvocact1[1]",
            "CSadvocact1[SQ02]": "CSadvocact1[2]",
            "CSadvocact1[SQ03]": "CSadvocact1[3]",
            "CSadvocact1[SQ04]": "CSadvocact1[4]",
            "CSadvocact1[SQ05]": "CSadvocact1[5]",
            "CSadvocact1[SQ06]": "CSadvocact1[6]",
            "CSadvocact1[SQ07]": "CSadvocact1[7]",
            "CSadvocact1[SQ08]": "CSadvocact1[8]",
            "CSadvocact2[SQ01]": "CSadvocact2[research]",
            "CSadvocact2[SQ02]": "CSadvocact2[consultations]",
            "CSadvocact2[SQ03]": "CSadvocact2[briefings]",
            "CSadvocact2[SQ04]": "CSadvocact2[expert_events]",
            "CSadvocact2[SQ05]": "CSadvocact2[participation_in_fora]",
            "CSadvocact2[SQ06]": "CSadvocact2[legal_opinions]",
            "CSadvocact2[SQ07]": "CSadvocact2[informal_encounters]",
            "CSadvocact2[SQ08]": "CSadvocact2[other]",
            "CSadvocimpact1[SQ01]": "CSadvocimpact1[increased_awareness]",
            "CSadvocimpact1[SQ02]": "CSadvocimpact1[policies_reflect_recommendations]",
            "CSadvocimpact1[SQ03]": "CSadvocimpact1[more_informed_debates]",
            "CSadvocimpact1[SQ04]": "CSadvocimpact1[achieved_goals]",
            "CSlitigateact1[SQ01]": "CSlitigateact1[1]",
            "CSlitigateact1[SQ02]": "CSlitigateact1[2]",
            "CSlitigateact1[SQ03]": "CSlitigateact1[3]",
            "CSlitigateact1[SQ04]": "CSlitigateact1[4]",
            "CSlitigateact1[SQ05]": "CSlitigateact1[5]",
            "CSlitigateact1[SQ06]": "CSlitigateact1[6]",
            "CSlitigateact1[SQ07]": "CSlitigateact1[7]",
            "CSlitigateact1[SQ08]": "CSlitigateact1[8]",
            "CSlitigateact2[SQ01]": "CSlitigateact2[initiating_lawsuit]",
            "CSlitigateact2[SQ02]": "CSlitigateact2[initiating_complaint]",
            "CSlitigateact2[SQ03]": "CSlitigateact2[supporting_existing_legislation]",
            "CSlitigateact2[SQ04]": "CSlitigateact2[other]",
            "CSlitigateimpact1[SQ01]": "CSlitigateimpact1[increased_awareness]",
            "CSlitigateimpact1[SQ02]": "CSlitigateimpact1[changed_the_law]",
            "CSlitigateimpact1[SQ03]": "CSlitigateimpact1[amendments_of_the_law]",
            "CSlitigateimpact1[SQ04]": "CSlitigateimpact1[revealed_new_information]",
            "CSlitigateimpact1[SQ05]": "CSlitigateimpact1[achieved_goals]",
            "CSprotectops1[SQ01]": "CSprotectops1[sectraining]",
            "CSprotectops1[SQ02]": "CSprotectops1[e2e]",
            "CSprotectops3[SQ01]": "CSprotectops3[encrypted_email]",
            "CSprotectops3[SQ02]": "CSprotectops3[vpn]",
            "CSprotectops3[SQ03]": "CSprotectops3[tor]",
            "CSprotectops3[SQ04]": "CSprotectops3[e2e_chat]",
            "CSprotectops3[SQ05]": "CSprotectops3[encrypted_hardware]",
            "CSprotectops3[SQ06]": "CSprotectops3[2fa]",
            "CSprotectops3[SQ07]": "CSprotectops3[other]",
            "CSprotectleg2A": "CSprotectleg2",
            "CSprotectleg3[SQ01]": "CSprotectleg3[free_counsel]",
            "CSprotectleg3[SQ02]": "CSprotectleg3[cost_insurance]",
            "CSprotectleg3[SQ03]": "CSprotectleg3[other]",
            "CScontstraintinter1": "CSconstraintinter1",
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
            "CSconstraintinter5ot": "CSconstraintinter5other",
            "CSconstraintinter6[SQ01]": "CSconstraintinter6[gender]",
            "CSconstraintinter6[SQ02]": "CSconstraintinter6[ethnicity]",
            "CSconstraintinter6[SQ03]": "CSconstraintinter6[political]",
            "CSconstraintinter6[SQ04]": "CSconstraintinter6[sexual]",
            "CSconstraintinter6[SQ05]": "CSconstraintinter6[religious]",
            "CSconstraintinter6[SQ06]": "CSconstraintinter6[other]",
            "CSconstraintinter6ot": "CSconstraintinter6other",
            "CSconstraintself1[SQ01]": "CSconstraintself1[avoid]",
            "CSconstraintself1[SQ02]": "CSconstraintself1[cancelled_campaign]",
            "CSconstraintself1[SQ03]": "CSconstraintself1[withdrew_litigation]",
            "CSconstraintself1[SQ04]": "CSconstraintself1[leave_profession]",
            "CSconstraintself1[SQ05]": "CSconstraintself1[other]",
            "CSconstraintself1oth": "CSconstraintself1other",
            "CSattitude3[SQ01]": "CSattitude3[rule_of_law]",
            "CSattitude3[SQ02]": "CSattitude3[civil_liberties]",
            "CSattitude3[SQ03]": "CSattitude3[effectiveness_of_intel]",
            "CSattitude3[SQ04]": "CSattitude3[legitimacy_of_intel]",
            "CSattitude3[SQ05]": "CSattitude3[trust_in_intel]",
            "CSattitude3[SQ06]": "CSattitude3[critique_of_intel]",
            "CSattitude3[SQ08]": "CSattitude3[prefer_not_to_say]",
            "CSgendersd": "CSgenderother",
        }
    )

    df = df.replace(to_replace=r"en", value="United Kingdom")
    df = df.replace(to_replace=r"de", value="Germany")
    df = df.replace(to_replace=r"fr", value="France")

    # Drop (very) incomplete surveys
    df = df[df["lastpage"] > 2]

    # Drop all but the columns needed for the analysis
    df = df[
        [
            "country",
            "lastpage",
            "CShr1",
            "CShr2",
            "CSexpertise1",
            "CSexpertise2",
            "CSexpertise3",
            "CSexpertise4",
            "CSfinance1",
            "CSfinance2[private_foundations]",
            "CSfinance2[donations]",
            "CSfinance2[national_public_funds]",
            "CSfinance2[corporate_sponsorship]",
            "CSfinance2[international_public_funds]",
            "CSfinance2[other]",
            "CSfinance2other",
            "CSfinance3",
            "CSfinance4",
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
            "CSfoi5other",
            "CSpreselection",
            "CScampact1[1]",
            "CScampact1[2]",
            "CScampact1[3]",
            "CScampact1[4]",
            "CScampact1[5]",
            "CScampact1[6]",
            "CScampact1[7]",
            "CScampact1[8]",
            "CScampact2[media_contributions]",
            "CScampact2[own_publications]",
            "CScampact2[petitions_open_letters]",
            "CScampact2[public_events]",
            "CScampact2[collaborations]",
            "CScampact2[demonstrations]",
            "CScampact2[social_media]",
            "CScampact2[advertising]",
            "CScampact2[volunteer_activities]",
            "CScampact2[providing_technical_tools]",
            "CScampact2[support_for_eu_campaigns]",
            "CScampact2[other]",
            "CScampact2other",
            "CScamptrans1",
            "CScamptrans2",
            "CScampimpact1[increased_awareness]",
            "CScampimpact1[policies_reflect_demands]",
            "CScampimpact1[created_media_attention]",
            "CScampimpact1[achieved_goals]",
            "CScampimpact2",
            "CSadvocact1[1]",
            "CSadvocact1[2]",
            "CSadvocact1[3]",
            "CSadvocact1[4]",
            "CSadvocact1[5]",
            "CSadvocact1[6]",
            "CSadvocact1[7]",
            "CSadvocact1[8]",
            "CSadvocact2[research]",
            "CSadvocact2[consultations]",
            "CSadvocact2[briefings]",
            "CSadvocact2[expert_events]",
            "CSadvocact2[participation_in_fora]",
            "CSadvocact2[legal_opinions]",
            "CSadvocact2[informal_encounters]",
            "CSadvocact2[other]",
            "CSadvocact2other",
            "CSadvoctrans1",
            "CSadvoctrans2",
            "CSadvocimpact1[increased_awareness]",
            "CSadvocimpact1[policies_reflect_recommendations]",
            "CSadvocimpact1[more_informed_debates]",
            "CSadvocimpact1[achieved_goals]",
            "CSadvocimpact2",
            "CSlitigateact1[1]",
            "CSlitigateact1[2]",
            "CSlitigateact1[3]",
            "CSlitigateact1[4]",
            "CSlitigateact1[5]",
            "CSlitigateact1[6]",
            "CSlitigateact1[7]",
            "CSlitigateact1[8]",
            "CSlitigateact2[initiating_lawsuit]",
            "CSlitigateact2[initiating_complaint]",
            "CSlitigateact2[supporting_existing_legislation]",
            "CSlitigateact2[other]",
            "CSlitigateact2other",
            "CSlitigatecost1",
            "CSlitigatecost2",
            "CSlitigatecost3",
            "CSlitigatetrans1",
            "CSlitigatetrans2",
            "CSlitigateimpact1[increased_awareness]",
            "CSlitigateimpact1[changed_the_law]",
            "CSlitigateimpact1[amendments_of_the_law]",
            "CSlitigateimpact1[revealed_new_information]",
            "CSlitigateimpact1[achieved_goals]",
            "CSlitigateimpact2",
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
            "CSprotectops3other",
            "CSprotectops4",
            "CSprotectleg1",
            "CSprotectleg2",
            "CSprotectleg2no",
            "CSprotectleg3[free_counsel]",
            "CSprotectleg3[cost_insurance]",
            "CSprotectleg3[other]",
            "CSprotectleg3other",
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
            "CSconstraintinter5other",
            "CSconstraintinter6[gender]",
            "CSconstraintinter6[ethnicity]",
            "CSconstraintinter6[political]",
            "CSconstraintinter6[sexual]",
            "CSconstraintinter6[religious]",
            "CSconstraintinter6[other]",
            "CSconstraintinter6other",
            "CSconstraintself1[avoid]",
            "CSconstraintself1[cancelled_campaign]",
            "CSconstraintself1[withdrew_litigation]",
            "CSconstraintself1[leave_profession]",
            "CSconstraintself1[other]",
            "CSconstraintself1other",
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
            "CSgender",
        ]
    ]

    # Set surveytype
    df["surveytype"] = "Civil Society Scrutiny"
    return df


###################################################################################
# Define base DataFrame
###################################################################################


df = get_cs_df()
df = df.reset_index(drop=True)


###################################################################################
# Make answers human-readable
###################################################################################


is_de = df.country == "Germany"
is_uk = df.country == "United Kingdom"
is_fr = df.country == "France"

df["CShr1"] = df["CShr1"].replace(
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

df["CSexpertise2"] = df["CSexpertise2"].replace(
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

df["CSexpertise3"] = df["CSexpertise3"].replace(
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

df["CSexpertise4"] = df["CSexpertise4"].replace(
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

df["CSfinance1"] = df["CSfinance1"].replace(
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


CSfinance2_options = [
    "private_foundations",
    "donations",
    "national_public_funds",
    "corporate_sponsorship",
    "international_public_funds",
    "other",
]
for label in CSfinance2_options:
    df[f"CSfinance2[{label}]"] = df[f"CSfinance2[{label}]"].replace(
        {
            "AO01": "Very important",
            "AO02": "Important",
            "AO03": "Somewhat important",
            "AO04": "Slightly important",
            "AO07": "No important at all",
            "AO09": "I don't know",
            "AO11": "I prefer not to say",
        }
    )

df["CSfinance4"] = df["CSfinance4"].replace(
    {
        "AO01": "Clearly beneficial for fundraising",
        "AO02": "Rather beneficial for fundraising",
        "AO03": "No effect on fundraising",
        "AO04": "Rather constraining for fundraising",
        "AO05": "Clearly constraining for fundraising",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["CSfoi1"] = df["CSfoi1"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

df["CSfoi3"] = df["CSfoi3"].replace(
    {
        "AO01": "Yes, within 30 days",
        "AO02": "No, usually longer than 30 days",
        "AO03": "Never",
        "AO04": "I don't know",
        "AO05": "I prefere not to say",
    }
)

df["CSfoi4"] = df["CSfoi4"].replace(
    {
        "AO01": "Very helpful",
        "AO03": "Helpful in parts",
        "AO05": "Not helpful at all",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["CSpreselection"] = df["CSpreselection"].replace(
    {
        "AO01": "Public Campaigning",
        "AO02": "Policy Advocacy",
        "AO03": "Strategic Litigation",
    }
)

CScampact2_options = [
    "media_contributions",
    "own_publications",
    "petitions_open_letters",
    "public_events",
    "collaborations",
    "demonstrations",
    "social_media",
    "advertising",
    "volunteer_activities",
    "providing_technical_tools",
    "support_for_eu_campaigns",
    "other",
]
for label in CScampact2_options:
    df[f"CScampact2[{label}]"] = df[f"CScampact2[{label}]"].replace(
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

df["CScamptrans1"] = df["CScamptrans1"].replace(
    {
        "AO01": "Always",
        "AO02": "Often (75% of the time)",
        "AO03": "Sometimes (50% of the time)",
        "AO04": "Rarely (25% of the time)",
        "AO05": "Never",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["CScamptrans2"] = df["CScamptrans2"].replace(
    {
        "AO01": "Always",
        "AO02": "Often (75% of the time)",
        "AO03": "Sometimes (50% of the time)",
        "AO04": "Rarely (25% of the time)",
        "AO05": "Never",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

CScampimpact1_options = [
    "increased_awareness",
    "policies_reflect_demands",
    "created_media_attention",
    "achieved_goals",
]
for label in CScampimpact1_options:
    df[f"CScampimpact1[{label}]"] = df[f"CScampimpact1[{label}]"].replace(
        {
            "AO01": "Agree completely",
            "AO02": "Agree to a great extent",
            "AO03": "Agree somewhat",
            "AO04": "Agree sligthly",
            "AO05": "Not agree at all",
            "AO06": "I don't know",
            "AO07": "I prefer not to say",
        }
    )

CSadvocact2_options = [
    "research",
    "consultations",
    "briefings",
    "expert_events",
    "participation_in_fora",
    "legal_opinions",
    "informal_encounters",
    "other",
]
for label in CSadvocact2_options:
    df[f"CSadvocact2[{label}]"] = df[f"CSadvocact2[{label}]"].replace(
        {
            "AO01": "Very important",
            "AO02": "Important",
            "AO03": "Somewhat important",
            "AO04": "Slightly important",
            "AO07": "Not important at all",
            "AO09": "I don't know",
            "AO11": "I prefer not to say",
        }
    )
    # Coding in LimeSurvey differs for UK
    df.loc[is_uk, f"CSadvocact2[{label}]"] = df[f"CSadvocact2[{label}]"].replace(
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


df["CSadvoctrans1"] = df["CSadvoctrans1"].replace(
    {
        "AO01": "Always",
        "AO02": "Often (75% of the time)",
        "AO03": "Sometimes (50% of the time)",
        "AO04": "Rarely (25% of the time)",
        "AO05": "Never",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["CSadvoctrans2"] = df["CSadvoctrans2"].replace(
    {
        "AO01": "Always",
        "AO02": "Often (75% of the time)",
        "AO03": "Sometimes (50% of the time)",
        "AO04": "Rarely (25% of the time)",
        "AO05": "Never",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

CSadvocimpact1_options = [
    "increased_awareness",
    "policies_reflect_recommendations",
    "more_informed_debates",
    "achieved_goals",
]
for label in CSadvocimpact1_options:
    df[f"CSadvocimpact1[{label}]"] = df[f"CSadvocimpact1[{label}]"].replace(
        {
            "AO01": "Agree completely",
            "AO42": "Agree to a great extent",
            "AO43": "Agree somewhat",
            "AO44": "Agree sligthly",
            "AO45": "Not agree at all",
            "AO46": "I don't know",
            "AO47": "I prefer not to say",
        }
    )
    # Here only DE survey is differenlty coded
    df.loc[is_de, f"CSadvocimpact1[{label}]"] = df[f"CSadvocimpact1[{label}]"].replace(
        {
            "AO01": "Agree completely",
            "AO02": "Agree to a great extent",
            "AO03": "Agree somewhat",
            "AO04": "Agree sligthly",
            "AO05": "Not agree at all",
            "AO06": "I don't know",
            "AO07": "I prefer not to say",
        }
    )

CSlitigateact2_options = [
    "initiating_lawsuit",
    "initiating_complaint",
    "supporting_existing_legislation",
    "other",
]
for label in CSlitigateact2_options:
    df[f"CSlitigateact2[{label}]"] = df[f"CSlitigateact2[{label}]"].replace(
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

df["CSlitigatetrans1"] = df["CSlitigatetrans1"].replace(
    {
        "AO01": "Always",
        "AO02": "Often (75% of the time)",
        "AO03": "Sometimes (50% of the time)",
        "AO04": "Rarely (25% of the time)",
        "AO05": "Never",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["CSlitigatetrans2"] = df["CSlitigatetrans2"].replace(
    {
        "AO01": "Always",
        "AO02": "Often (75% of the time)",
        "AO03": "Sometimes (50% of the time)",
        "AO04": "Rarely (25% of the time)",
        "AO05": "Never",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

CSlitigateimpact1_options = [
    "increased_awareness",
    "changed_the_law",
    "amendments_of_the_law",
    "revealed_new_information",
    "achieved_goals",
]
for label in CSlitigateimpact1_options:
    df[f"CSlitigateimpact1[{label}]"] = df[f"CSlitigateimpact1[{label}]"].replace(
        {
            "AO01": "Agree completely",
            "AO42": "Agree to a great extent",
            "AO43": "Agree somewhat",
            "AO44": "Agree sligthly",
            "AO45": "Not agree at all",
            "AO46": "I don't know",
            "AO47": "I prefer not to say",
        }
    )

    df.loc[is_de, f"CSlitigateimpact1[{label}]"] = df[
        f"CSlitigateimpact1[{label}]"
    ].replace(
        {
            "AO01": "Agree completely",
            "AO02": "Agree to a great extent",
            "AO03": "Agree somewhat",
            "AO04": "Agree sligthly",
            "AO05": "Not agree at all",
            "AO06": "I don't know",
            "AO07": "I prefer not to say",
        }
    )

for i in range(1, 3):
    df[f"CSlitigatecost{i}"] = df[f"CSlitigatecost{i}"].replace(
        {
            "AO01": "Always or very often",
            "AO02": "Often (75% of the time)",
            "AO03": "Sometimes (50% of the time)",
            "AO04": "Rarely (25% of the time)",
            "AO05": "Never or rarely",
            "AO06": "I don't know",
            "AO07": "I prefer not to say",
        }
    )

df["CSlitigatecost3"] = df["CSlitigatecost3"].replace(
    {
        "AO01": "Not risky at all",
        "AO02": "Somewaht risky",
        "AO03": "Very risky",
        "AO04": "I don't know",
        "AO05": "I prefer not to say",
    }
)

for label in [
    "sectraining",
    "e2e",
]:
    df[f"CSprotectops1[{label}]"] = df[f"CSprotectops1[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

df["CSprotectops2"] = df["CSprotectops2"].replace(
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

    df.loc[(is_uk | is_fr), f"CSprotectops3[{label}]"] = df[
        f"CSprotectops3[{label}]"
    ].replace(
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
    df.loc[is_de, f"CSprotectops3[{label}]"] = df[f"CSprotectops3[{label}]"].replace(
        {
            "AO01": "Very important",
            "AO02": "Important",
            "AO03": "Somewhat important",
            "AO04": "Slightly important",
            "AO07": "Not important at all",
            "AO09": "I don't know",
            "AO11": "I prefer not to say",
        }
    )


df["CSprotectops4"] = df["CSprotectops4"].replace(
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

df["CSprotectleg1"] = df["CSprotectleg1"].replace(
    {
        "AO01": "Always",
        "AO02": "Often (75% of the time)",
        "AO03": "Sometimes (50% of the time)",
        "AO04": "Rarely (25% of the time)",
        "AO05": "Never",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["CSprotectleg2"] = df["CSprotectleg2"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

for label in ["free_counsel", "cost_insurance", "other"]:
    df[f"CSprotectleg3[{label}]"] = df[f"CSprotectleg3[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

df["CSconstraintinter1"] = df["CSconstraintinter1"].replace(
    {
        "AO01": "Yes, I have evidence",
        "AO02": "Yes, I suspect",
        "AO03": "No",
        "AO04": "I don't know",
        "AO05": "I prefer not to say",
    }
)

df["CSconstraintinter2"] = df["CSconstraintinter2"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

df["CSconstraintinter3"] = df["CSconstraintinter3"].replace(
    {
        "AO01": "I was threatened with prosecution",
        "AO02": "I was prosecuted but acquitted",
        "AO03": "I was prosecuted and convicted",
        "AO04": "I don't know",
        "AO05": "I prefer not to say",
    }
)

CSconstraintinter4_options = [
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
for label in CSconstraintinter4_options:
    df[f"CSconstraintinter4[{label}]"] = df[f"CSconstraintinter4[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

CSconstraintinter5_options = ["unsolicited_information", "invitations", "other"]
for label in CSconstraintinter5_options:
    df[f"CSconstraintinter5[{label}]"] = df[f"CSconstraintinter5[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

CSconstraintinter6_options = [
    "gender",
    "ethnicity",
    "political",
    "sexual",
    "religious",
    "other",
]
for label in CSconstraintinter6_options:
    df[f"CSconstraintinter6[{label}]"] = df[f"CSconstraintinter6[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

CSconstraintself1_options = [
    "avoid",
    "cancelled_campaign",
    "withdrew_litigation",
    "leave_profession",
    "other",
]
for label in CSconstraintself1_options:
    df[f"CSconstraintself1[{label}]"] = df[f"CSconstraintself1[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

df["CSattitude1"] = df["CSattitude1"].replace(
    {
        "AO01": "Intelligence agencies are incompatible with democratic <br>values and should be abolished",
        "AO02": "Intelligence agencies contradict democratic principles,<br>and their powers should be kept at a bare minimum",
        "AO03": "Intelligence agencies are necessary and legitimate institutions <br>of democratic states, even though they may sometimes overstep <br>their legal mandates",
        "AO04": "Intelligence agencies are a vital component of national <br>security and should be shielded from excessive bureaucratic <br>restrictions",
        "AO05": "I prefer not to say",
    }
)

df["CSattitude2"] = df["CSattitude2"].replace(
    {
        "AO01": "Intelligence oversight generally succeeds in uncovering <br>past misconduct and preventing future misconduct",
        "AO02": "Intelligence oversight is mostly effective, however its <br>institutional design needs reform for oversight practitioners to reliably <br>uncover past misconduct and prevent future misconduct",
        "AO03": "Intelligence oversight lacks efficacy, hence a fundamental <br>reorganization of oversight capacity is needed for oversight practitioners <br>to reliably uncover past misconduct and prevent future misconduct",
        "AO04": "Effective intelligence oversight is a hopeless endeavour <br>and even a systematic reorganization is unlikely to ensure <br>misconduct is uncovered and prevented.",
        "AO05": "I prefer not to say",
    }
)

for i in range(4, 7):
    for j in range(1, 7):
        df[f"CSattitude{i}[{j}]"] = df[f"CSattitude{i}[{j}]"].replace(
            {
                "AO01": "Parliamentary oversight bodies",
                "AO02": "Judicial oversight bodies",
                "AO03": "Independent expert bodies",
                "AO04": "Data protection authorities",
                "AO05": "Audit courts",
                "AO06": "The media",
            }
        )
        # Here, FR is coded differently
        df.loc[is_fr, f"CSattitude{i}[{j}]"] = df[f"CSattitude{i}[{j}]"].replace(
            {
                "AO01": "Parliamentary oversight bodies",
                "AO02": "Judicial oversight bodies",
                "AO03": "Independent expert bodies",
                "AO04": "Data protection authorities",
                "AO07": "Audit courts",
                "AO06": "Media organisations",
            }
        )

df["CSgender"] = df["CSgender"].replace(
    {
        "AO01": "Woman",
        "AO02": "Non-binary",
        "AO03": "Man",
        "AO04": "I prefer not to say",
        "AO05": "Other",
    }
)
###############################################################################
# Make answers analysable (change data types etc.)
###############################################################################


df["CShr2"] = df["CShr2"].replace("?", np.nan)
df["CShr2"] = df["CShr2"].replace("0,5", 0.5)
df["CShr2"] = pd.to_numeric(df["CShr2"], errors="coerce")

df["CSexpertise1"] = df["CSexpertise1"].replace("?", np.nan)
df["CSexpertise1"] = df["CSexpertise1"].replace("<1", 0.5)
df["CSexpertise1"] = pd.to_numeric(df["CSexpertise1"], errors="coerce")

df["CSfoi2"] = df["CSfoi2"].replace(
    {"20+": 20.0, " ca 10": 10.0, "several": 3.0, "15+": 15.0}
)
df["CSfoi2"] = pd.to_numeric(df["CSfoi2"], errors="coerce")

# Here, I change the datatype to boolean for all the multiple choice answers
for col in df:
    if (
        col.startswith("CShr3")
        or col.startswith("CSfoi5[")
        or col.startswith("CSsoc5[")
        or col.startswith("CSsoc6[")
        or col.startswith("CSimpact1[")
        or col.startswith("CSimpact2[")
        or col.startswith("CSattitude3[")
    ):
        df[col] = df[col].replace(np.nan, False)
        df[col] = df[col].replace("Y", True)
        df[col] = df[col].astype("bool")


###############################################################################
# Sidebar | Filter logic
###############################################################################

# This is getting triggered when section is changed
def callback():
    st.experimental_set_query_params(section=st.session_state.section)


sections = [
    "Overview",
    "Resources",
    "Public Campaigning",
    "Policy Advocacy",
    "Strategic Litigation",
    "Protection",
    "Constraints",
    "Attitudes",
    "Appendix",
]

try:
    query_params = st.experimental_get_query_params()
    query_section = query_params["section"][0]
    if "section" not in st.session_state:
        st.session_state.section = query_section

except KeyError:
    st.experimental_set_query_params(section=sections[0])
    query_params = st.experimental_get_query_params()
    query_section = query_params["section"][0]
    if "section" not in st.session_state:
        st.session_state.section = query_section

selected_section = st.sidebar.radio(
    "Choose section",
    sections,
    index=sections.index(query_section),
    key="section",
    on_change=callback
)

st.write(selected_section)

filters = {
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
# Save a useful snapshot of the data (comment out for production)
###############################################################################


df.to_pickle("./data/civsoc.pkl")
df.to_excel("./data/civsoc.xlsx")
df.to_csv("./data/civsoc.csv")


###############################################################################
# Custom JS/CSS
###############################################################################

# This causes the page to scroll to top when section is changed
components.html(
    f"""
        <!--{st.session_state.section}-->
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
        </script>
    """,
    height=0
)

st.markdown(
    """ <style> h3 {line-height: 1.3} </style> """,
    unsafe_allow_html=True,
)


###############################################################################
# Display dynamic charts
###############################################################################


st.title("IOI Survey Data Explorer")
st.write("... of the responses given by __civil society organisation__ representatives")

if selected_section == "Overview":
    st.write("# Overview")

    merged_markdown = read_markdown_file("explorer/markdown/media.md")
    st.markdown(merged_markdown, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.metric("Civil Society Representatives", len(df[filter].index))
    col2.metric(
        "Cumulative years spent working on SBIA",
        int(df[filter]["CSexpertise1"].sum()),
    )

    st.write("### Country `[country]`")
    country_counts = df[filter]["country"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=country_counts,
            names=country_counts.index,
        )
    )

    st.write("### Predominant activity `[CSpreselect]`")
    CSpreselection_counts = df[filter]["CSpreselection"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSpreselection_counts,
            names=CSpreselection_counts.index,
        )
    )

if selected_section == "Resources":
    st.write("# Resources")

    st.write("## Human Resources")

    st.write("### What is your employment status `[CShr1]`")
    CShr1_counts = df[filter]["CShr1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            CShr1_counts,
            values=CShr1_counts,
            names=CShr1_counts.index,
            color=CShr1_counts.index,
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
        "### How many days per month do you work on surveillance by intelligence agencies? `[CShr2]`"
    )
    st.plotly_chart(
        render_histogram(
            df=df[filter],
            x="CShr2",
            y=None,
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"CShr2": "days per month"},
        )
    )

    st.plotly_chart(
        render_boxplot(
            df=df[filter],
            points="all",
            x="country",
            y="CShr2",
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
        )
    )

    st.write("## Expertise")

    st.write(
        "### How many years have you spent working on surveillance by intelligence agencies? `[CSexpertise1]`"
    )
    st.plotly_chart(
        render_histogram(
            df[filter],
            x="CSexpertise1",
            y=None,
            nbins=20,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"CSexpertise1": "years"},
        )
    )

    st.plotly_chart(
        render_boxplot(
            df=df[filter],
            points="all",
            x="country",
            y="CSexpertise1",
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
        )
    )

    st.write(
        "### How do you assess your level of expertise concerning the **legal** aspects of surveillance by intelligence agencies? For example, knowledge of intelligence law, case law. `[CSexpertise2]`"
    )
    CSexpertise2_counts = df[filter]["CSexpertise2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSexpertise2_counts,
            names=CSexpertise2_counts.index,
            color_discrete_sequence=None,
            color=CSexpertise2_counts.index,
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
        "### How do you assess your level of expertise concerning the **political** aspects of surveillance by intelligence agencies?` [CSexpertise3]`"
    )
    CSexpertise3_counts = df[filter]["CSexpertise3"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSexpertise3_counts,
            names=CSexpertise3_counts.index,
            color_discrete_sequence=None,
            color=CSexpertise3_counts.index,
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
        "### How do you assess your level of expertise concerning the **technical** aspects of surveillance by intelligence agencies?` [CSexpertise4]`"
    )
    CSexpertise4_counts = df[filter]["CSexpertise4"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSexpertise4_counts,
            names=CSexpertise4_counts.index,
            color_discrete_sequence=None,
            color=CSexpertise4_counts.index,
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
        "### How do you assess the financial resources that have been available for your work on intelligence over the past 5 years? `[CSfinance1]`"
    )
    CSfinance1_counts = df[filter]["CSfinance1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSfinance1_counts,
            names=CSfinance1_counts.index,
            color_discrete_sequence=None,
            color=CSfinance1_counts.index,
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

    st.write(
        "### How important are the following funding categories for your organisation's work on intelligence-related issues? `[CSfinance2]`"
    )
    CSfinance2_options = [
        "Private foundations",
        "Donations",
        "National public funds",
        "Corporate sponsorships",
        "International public funds",
        "Other",
    ]
    CSfinance2_very_important = []
    CSfinance2_somewhat_important = []
    CSfinance2_important = []
    CSfinance2_slightly_important = []
    CSfinance2_not_important = []
    for importance in [
        "Very important",
        "Somewhat important",
        "Important",
        "Slightly important",
        "Not important at all",
    ]:
        for label in [
            "private_foundations",
            "donations",
            "national_public_funds",
            "corporate_sponsorship",
            "international_public_funds",
            "other",
        ]:
            try:
                count = df[filter][f"CSfinance2[{label}]"].value_counts()[importance]
            except KeyError:
                count = 0
            if importance == "Very important":
                CSfinance2_very_important.append(count)
            elif importance == "Somewhat important":
                CSfinance2_somewhat_important.append(count)
            elif importance == "Important":
                CSfinance2_important.append(count)
            elif importance == "Slightly important":
                CSfinance2_slightly_important.append(count)
            elif importance == "Not important at all":
                CSfinance2_not_important.append(count)
            else:
                continue

    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Very important",
                    x=CSfinance2_options,
                    y=CSfinance2_very_important,
                    marker_color="#581845",
                ),
                go.Bar(
                    name="Somewhat important",
                    x=CSfinance2_options,
                    y=CSfinance2_somewhat_important,
                    marker_color="#900C3F",
                ),
                go.Bar(
                    name="Important",
                    x=CSfinance2_options,
                    y=CSfinance2_important,
                    marker_color="#C70039",
                ),
                go.Bar(
                    name="Slightly important",
                    x=CSfinance2_options,
                    y=CSfinance2_slightly_important,
                    marker_color="#FF5733",
                ),
                go.Bar(
                    name="Not important at all",
                    x=CSfinance2_options,
                    y=CSfinance2_not_important,
                    marker_color="#FFC300",
                ),
            ],
        )
    )

    st.write("### If you selected ‘other’, please specify `[CSfinance2other]`")
    for i in df[filter]["CSfinance2other"].to_list():
        if type(i) != float:
            st.write("- " + i.replace("\n", " "))

    st.write(
        "### Looking at the past year, which source of funding was most important in enabling you to work on intelligence-related issues? `[CSfinance3]`"
    )
    for i in df[filter]["CSfinance3"].to_list():
        if type(i) != float:
            st.write("- " + i.replace("\n", " ").replace("-", ""))

    st.write(
        "### What effect did your work on surveillance by intelligence agencies have for your organisation’s fundraising over the past 5 years? `[CSfinance4]`"
    )
    CSfinance4_counts = df[filter]["CSfinance4"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSfinance4_counts,
            names=CSfinance4_counts.index,
            color_discrete_sequence=None,
            color=CSfinance4_counts.index,
            color_discrete_map={
                "Clearly beneficial for fundraising": px.colors.qualitative.Prism[9],
                "Rather beneficial for fundraising": px.colors.qualitative.Prism[8],
                "No effect on fundraising": px.colors.qualitative.Prism[7],
                "Rather constraining for fundraising": px.colors.qualitative.Prism[6],
                "Clearly constraining for fundraising": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write("## Freedom of Information")

    st.write(
        "### Have you requested information under the national Freedom of Information Law  when you worked on intelligence-related issues over the past 5 years? `[CSfoi1]`"
    )
    CSfoi1_counts = df[filter]["CSfoi1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            CSfoi1_counts,
            values=CSfoi1_counts,
            names=CSfoi1_counts.index,
            color=CSfoi1_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write("### How often did you request information? `[CSfoi2]`")
    st.plotly_chart(
        render_histogram(
            df[filter],
            x="CSfoi2",
            y=None,
            nbins=10,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"CSfoi2": "Number of requests"},
        )
    )

    st.plotly_chart(
        render_boxplot(
            df=df[filter],
            points="all",
            x="country",
            y="CSfoi2",
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
        )
    )

    st.write(
        "### Over the past 5 years, did you receive a response to your FOI request(s) in a timely manner? `[CSfoi3]`"
    )
    CSfoi3_counts = df[filter]["CSfoi3"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            CSfoi3_counts,
            values=CSfoi3_counts,
            names=CSfoi3_counts.index,
            color=CSfoi3_counts.index,
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
        "### How helpful have FOI requests been for your work on intelligence-related issues? `[CSfoi4]`"
    )
    foi4_counts = df[filter]["CSfoi4"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=foi4_counts,
            names=foi4_counts.index,
        )
    )

    st.write(
        "### Why haven’t you requested information under the national FOI law when you reported on intelligence-related issues over the past 5 years? `[CSfoi5]`"
    )
    CSfoi5_df = pd.DataFrame(columns=("option", "count", "country"))
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
        CSfoi5_data = df[filter]["country"][df[f"CSfoi5[{label}]"] == 1].tolist()
        for i in CSfoi5_data:
            CSfoi5_df = CSfoi5_df.append(
                {"option": label, "count": CSfoi5_data.count(i), "country": i},
                ignore_index=True,
            )
    CSfoi5_df = CSfoi5_df.drop_duplicates()
    st.plotly_chart(
        render_histogram(
            CSfoi5_df,
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

if selected_section == "Public Campaigning":

    st.write("## Activity")

    st.write(
        "### Please list the public campaigns concerning surveillance by intelligence agencies that your organisation has conducted within the past 5 years. `[CScampact1]`"
    )
    for j in range(1, 9):
        for i in list(set(df[filter][f"CScampact1[{j}]"].to_list())):
            if type(i) != float:
                st.write("- " + i)

    st.write(
        "### How important are the following campaigning tools for your work concerning intelligence-related issues? `[CScampact2]`"
    )
    CScampact2_options = [
        "Media contributions",
        "Own publications",
        "Petitions and open letters",
        "Public events",
        "Collaborations with celebrities and influencers",
        "Demonstrations and rallies",
        "Social media communications",
        "Advertising",
        "Volunteer activities",
        "Providing technical tools",
        "Support for campaign activities in other countries",
        "Other",
    ]
    CScampact2_very_important = []
    CScampact2_somewhat_important = []
    CScampact2_important = []
    CScampact2_slightly_important = []
    CScampact2_not_important = []
    for importance in [
        "Very important",
        "Somewhat important",
        "Important",
        "Slightly important",
        "Not important at all",
    ]:
        for label in [
            "media_contributions",
            "own_publications",
            "petitions_open_letters",
            "public_events",
            "collaborations",
            "demonstrations",
            "social_media",
            "advertising",
            "volunteer_activities",
            "providing_technical_tools",
            "support_for_eu_campaigns",
            "other",
        ]:
            try:
                count = df[filter][f"CScampact2[{label}]"].value_counts()[importance]
            except KeyError:
                count = 0
            if importance == "Very important":
                CScampact2_very_important.append(count)
            elif importance == "Somewhat important":
                CScampact2_somewhat_important.append(count)
            elif importance == "Important":
                CScampact2_important.append(count)
            elif importance == "Slightly important":
                CScampact2_slightly_important.append(count)
            elif importance == "Not important at all":
                CScampact2_not_important.append(count)
            else:
                continue

    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Very important",
                    x=CScampact2_options,
                    y=CScampact2_very_important,
                    marker_color="#581845",
                ),
                go.Bar(
                    name="Somewhat important",
                    x=CScampact2_options,
                    y=CScampact2_somewhat_important,
                    marker_color="#900C3F",
                ),
                go.Bar(
                    name="Important",
                    x=CScampact2_options,
                    y=CScampact2_important,
                    marker_color="#C70039",
                ),
                go.Bar(
                    name="Slightly important",
                    x=CScampact2_options,
                    y=CScampact2_slightly_important,
                    marker_color="#FF5733",
                ),
                go.Bar(
                    name="Not important at all",
                    x=CScampact2_options,
                    y=CScampact2_not_important,
                    marker_color="#FFC300",
                ),
            ],
        )
    )

    campact2other_list = df[filter]["CScampact2other"].dropna().to_list()
    st.write("### If you selected ‘other’, please specify `[CScampact2other]`")
    if len(campact2other_list) > 0:
        for i in campact2other_list:
            if type(i) != float:
                st.write("- " + i)
    else:
        st.write("_no answers given_")

    st.write("## Transnational Scope")

    st.write(
        "### How frequently do your public campaigns address transnational issues of surveillance by intelligence agencies? `[CScamptrans1]`"
    )
    CScamptrans1_counts = df[filter]["CScamptrans1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CScamptrans1_counts,
            names=CScamptrans1_counts.index,
            color=CScamptrans1_counts.index,
            color_discrete_map={
                "Always": px.colors.qualitative.Prism[9],
                "Often (75% of the time)": px.colors.qualitative.Prism[8],
                "Sometimes (50% of the time)": px.colors.qualitative.Prism[7],
                "Rarely (25% of the time)": px.colors.qualitative.Prism[6],
                "Never": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write(
        "### When conducting public campaigns on surveillance by intelligence agencies, how often do you collaborate with civil society actors in other countries? `[CScamptrans2]`"
    )
    CScamptrans2_counts = df[filter]["CScamptrans2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CScamptrans2_counts,
            names=CScamptrans2_counts.index,
            color=CScamptrans2_counts.index,
            color_discrete_map={
                "Always": px.colors.qualitative.Prism[9],
                "Often (75% of the time)": px.colors.qualitative.Prism[8],
                "Sometimes (50% of the time)": px.colors.qualitative.Prism[7],
                "Rarely (25% of the time)": px.colors.qualitative.Prism[6],
                "Never": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write("## Perceived Impact")

    st.write(
        "### How much do you agree with the following statements concerning the effectiveness of your campaigning activities regarding intelligence-related issues over the past 5 years? `[CScampimpact1]`"
    )
    CScampimpact1_labels = [
        "Helped increase public awareness",
        "Our demands have been reflected in politics",
        "Created media attention",
        "Achieved defined goals",
    ]
    CScampimpact1_agree_completely = []
    CScampimpact1_agree_to_great_extent = []
    CScampimpact1_agree_somewhat = []
    CScampimpact1_agree_slightly = []
    CScampimpact1_not_agree_at_all = []
    for agreement in [
        "Agree completely",
        "Agree to a great extent",
        "Agree somewhat",
        "Agree slightly",
        "Not agree at all",
    ]:
        for label in CScampimpact1_options:
            try:
                count = df[filter][f"CScampimpact1[{label}]"].value_counts()[agreement]
            except KeyError:
                count = 0
            if agreement == "Agree completely":
                CScampimpact1_agree_completely.append(count)
            elif agreement == "Agree to a great extent":
                CScampimpact1_agree_to_great_extent.append(count)
            elif agreement == "Agree somewhat":
                CScampimpact1_agree_somewhat.append(count)
            elif agreement == "Agree slightly":
                CScampimpact1_agree_slightly.append(count)
            elif agreement == "Not agree at all":
                CScampimpact1_not_agree_at_all.append(count)
            else:
                continue
    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Agree completely",
                    x=CScampimpact1_labels,
                    y=CScampimpact1_agree_completely,
                    marker_color="#581845",
                ),
                go.Bar(
                    name="Agree to a great extent",
                    x=CScampimpact1_labels,
                    y=CScampimpact1_agree_to_great_extent,
                    marker_color="#900C3F",
                ),
                go.Bar(
                    name="Agree somewhat",
                    x=CScampimpact1_labels,
                    y=CScampimpact1_agree_somewhat,
                    marker_color="#C70039",
                ),
                go.Bar(
                    name="Agree slightly",
                    x=CScampimpact1_labels,
                    y=CScampimpact1_agree_slightly,
                    marker_color="#FF5733",
                ),
                go.Bar(
                    name="Not agree at all",
                    x=CScampimpact1_labels,
                    y=CScampimpact1_not_agree_at_all,
                    marker_color="#FFC300",
                ),
            ],
        )
    )

    CScampimpact2_list = df[filter]["CScampimpact2"].dropna().to_list()
    st.write(
        "### Please give an example for the impact that you see, such as references to your campaigning materials, same or similar wording or narratives used in official documents, personal feedback you received, online statistics, etc. `[CScampimpact2]`"
    )
    if len(CScampimpact2_list) > 0:
        for i in CScampimpact2_list:
            if type(i) != float:
                st.write("- " + i)
    else:
        st.write("_no answers given_")

if selected_section == "Policy Advocacy":
    st.write("## Activity")

    st.write(
        "### Please list the policy advocacy activities (e.g. lobbying and research) concerning surveillance by intelligence agencies that your organisation has conducted within the past 5 years. `[CSadvocact1]`"
    )
    CSadvocact1_list = list()
    for j in range(1, 9):
        for i in df[filter][f"CSadvocact1[{j}]"].fillna("_no answer given_").to_list():
            CSadvocact1_list.append(i)
    CSadvocact1_list = list(set(CSadvocact1_list))
    if len(CSadvocact1_list) > 1:
        for answer in CSadvocact1_list:
            if answer != "_no answer given_":
                st.write("- " + answer)
    else:
        st.write(CSadvocact1_list[0])

    st.write(
        "### How important are the following policy advocacy tools for your work on intelligence-related issues? `[CSadvocact2]`"
    )
    CSadvocact2_labels = [
        "Research & analysis",
        "Contributing to consultations",
        "Briefing of policy makers",
        "Expert events",
        "Participation in fora or bodies",
        "Legal opinions",
        "Informal encounters",
        "Other",
    ]
    CSadvocact2_very_important = []
    CSadvocact2_somewhat_important = []
    CSadvocact2_important = []
    CSadvocact2_slightly_important = []
    CSadvocact2_not_important = []
    for importance in [
        "Very important",
        "Somewhat important",
        "Important",
        "Slightly important",
        "Not important at all",
    ]:
        for option in CSadvocact2_options:
            try:
                count = df[filter][f"CSadvocact2[{option}]"].value_counts()[importance]
            except KeyError:
                count = 0
            if importance == "Very important":
                CSadvocact2_very_important.append(count)
            elif importance == "Somewhat important":
                CSadvocact2_somewhat_important.append(count)
            elif importance == "Important":
                CSadvocact2_important.append(count)
            elif importance == "Slightly important":
                CSadvocact2_slightly_important.append(count)
            elif importance == "Not important at all":
                CSadvocact2_not_important.append(count)
            else:
                continue

    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Very important",
                    x=CSadvocact2_labels,
                    y=CSadvocact2_very_important,
                    marker_color="#581845",
                ),
                go.Bar(
                    name="Somewhat important",
                    x=CSadvocact2_labels,
                    y=CSadvocact2_somewhat_important,
                    marker_color="#900C3F",
                ),
                go.Bar(
                    name="Important",
                    x=CSadvocact2_labels,
                    y=CSadvocact2_important,
                    marker_color="#C70039",
                ),
                go.Bar(
                    name="Slightly important",
                    x=CSadvocact2_labels,
                    y=CSadvocact2_slightly_important,
                    marker_color="#FF5733",
                ),
                go.Bar(
                    name="Not important at all",
                    x=CSadvocact2_labels,
                    y=CSadvocact2_not_important,
                    marker_color="#FFC300",
                ),
            ],
        )
    )

    campact2other_list = df[filter]["CSadvocact2other"].dropna().to_list()
    st.write("### If you selected ‘other’, please specify `[CSadvocact2other]`")
    if len(campact2other_list) > 0:
        for i in campact2other_list:
            if type(i) != float:
                st.write("- " + i)
    else:
        st.write("_no answers given_")

    st.write("## Transnational Scope")

    st.write(
        "### How frequently does your policy advocacy address transnational issues of surveillance by intelligence agencies? `[CSadvoctrans1]`"
    )
    CSadvoctrans1_counts = df[filter]["CSadvoctrans1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSadvoctrans1_counts,
            names=CSadvoctrans1_counts.index,
            color=CSadvoctrans1_counts.index,
            color_discrete_map={
                "Always": px.colors.qualitative.Prism[9],
                "Often (75% of the time)": px.colors.qualitative.Prism[8],
                "Sometimes (50% of the time)": px.colors.qualitative.Prism[7],
                "Rarely (25% of the time)": px.colors.qualitative.Prism[6],
                "Never": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write(
        "### When performing policy advocacy concerning surveillance by intelligence agencies, how often do you collaborate with civil society actors in other countries? `[CSadvoctrans2]`"
    )
    CSadvoctrans2_counts = df[filter]["CSadvoctrans2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSadvoctrans2_counts,
            names=CSadvoctrans2_counts.index,
            color=CSadvoctrans2_counts.index,
            color_discrete_map={
                "Always": px.colors.qualitative.Prism[9],
                "Often (75% of the time)": px.colors.qualitative.Prism[8],
                "Sometimes (50% of the time)": px.colors.qualitative.Prism[7],
                "Rarely (25% of the time)": px.colors.qualitative.Prism[6],
                "Never": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write("## Perceived Impact")

    st.write(
        "### How much do you agree with the following statements concerning the effectiveness of your advocacy activities regarding intelligence-related issues over the past 5 years? `[CSadvocimpact1]`"
    )
    CSadvocimpact1_labels = [
        "Helped increase public awareness",
        "Our policy recommendations have been reflected in politics",
        "Contributed to more informed debate",
        "Achieved defined goals",
    ]
    CSadvocimpact1_agree_completely = []
    CSadvocimpact1_agree_to_great_extent = []
    CSadvocimpact1_agree_somewhat = []
    CSadvocimpact1_agree_slightly = []
    CSadvocimpact1_not_agree_at_all = []
    for agreement in [
        "Agree completely",
        "Agree to a great extent",
        "Agree somewhat",
        "Agree slightly",
        "Not agree at all",
    ]:
        for label in CSadvocimpact1_options:
            try:
                count = df[filter][f"CSadvocimpact1[{label}]"].value_counts()[agreement]
            except KeyError:
                count = 0
            if agreement == "Agree completely":
                CSadvocimpact1_agree_completely.append(count)
            elif agreement == "Agree to a great extent":
                CSadvocimpact1_agree_to_great_extent.append(count)
            elif agreement == "Agree somewhat":
                CSadvocimpact1_agree_somewhat.append(count)
            elif agreement == "Agree slightly":
                CSadvocimpact1_agree_slightly.append(count)
            elif agreement == "Not agree at all":
                CSadvocimpact1_not_agree_at_all.append(count)
            else:
                continue
    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Agree completely",
                    x=CSadvocimpact1_labels,
                    y=CSadvocimpact1_agree_completely,
                    marker_color="#581845",
                ),
                go.Bar(
                    name="Agree to a great extent",
                    x=CSadvocimpact1_labels,
                    y=CSadvocimpact1_agree_to_great_extent,
                    marker_color="#900C3F",
                ),
                go.Bar(
                    name="Agree somewhat",
                    x=CSadvocimpact1_labels,
                    y=CSadvocimpact1_agree_somewhat,
                    marker_color="#C70039",
                ),
                go.Bar(
                    name="Agree slightly",
                    x=CSadvocimpact1_labels,
                    y=CSadvocimpact1_agree_slightly,
                    marker_color="#FF5733",
                ),
                go.Bar(
                    name="Not agree at all",
                    x=CSadvocimpact1_labels,
                    y=CSadvocimpact1_not_agree_at_all,
                    marker_color="#FFC300",
                ),
            ],
        )
    )

    CSadvocimpact2_list = df[filter]["CSadvocimpact2"].dropna().to_list()
    st.write(
        "### Please give an example for the impact that you see, such as references to your materials, same or similar wording used in official documents, personal feedback you received, etc. `[CSadvocimpact2]`"
    )
    if len(CSadvocimpact2_list) > 0:
        for i in CSadvocimpact2_list:
            if type(i) != float:
                st.write("- " + i)
    else:
        st.write("_no answers given_")

if selected_section == "Strategic Litigation":
    st.write("## Activity")

    st.write(
        "### Please name the cases of strategic litigation concerning surveillance by intelligence agencies that your CSO has participated in within the past 5 years. `[CSlitigateact1]`"
    )
    CSlitigateact1_list = list()
    for j in range(1, 9):
        for i in (
            df[filter][f"CSlitigateact1[{j}]"].fillna("_no answer given_").to_list()
        ):
            CSlitigateact1_list.append(i)
    CSlitigateact1_list = list(set(CSlitigateact1_list))
    if len(CSlitigateact1_list) > 1:
        for answer in CSlitigateact1_list:
            if answer != "_no answer given_":
                st.write("- " + answer)
    else:
        st.write(CSlitigateact1_list[0])

    st.write(
        "### How important are the following policy litigateacy tools for your work on intelligence-related issues? `[CSlitigateact2]`"
    )
    CSlitigateact2_labels = [
        "Initiating and/or coordinating a lawsuit",
        "Initiating a legal complaint",
        "Supporting existing legislation",
        "Other",
    ]
    CSlitigateact2_very_important = []
    CSlitigateact2_somewhat_important = []
    CSlitigateact2_important = []
    CSlitigateact2_slightly_important = []
    CSlitigateact2_not_important = []
    for importance in [
        "Very important",
        "Somewhat important",
        "Important",
        "Slightly important",
        "Not important at all",
    ]:
        for option in CSlitigateact2_options:
            try:
                count = df[filter][f"CSlitigateact2[{option}]"].value_counts()[
                    importance
                ]
            except KeyError:
                count = 0
            if importance == "Very important":
                CSlitigateact2_very_important.append(count)
            elif importance == "Somewhat important":
                CSlitigateact2_somewhat_important.append(count)
            elif importance == "Important":
                CSlitigateact2_important.append(count)
            elif importance == "Slightly important":
                CSlitigateact2_slightly_important.append(count)
            elif importance == "Not important at all":
                CSlitigateact2_not_important.append(count)
            else:
                continue

    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Very important",
                    x=CSlitigateact2_labels,
                    y=CSlitigateact2_very_important,
                    marker_color="#581845",
                ),
                go.Bar(
                    name="Somewhat important",
                    x=CSlitigateact2_labels,
                    y=CSlitigateact2_somewhat_important,
                    marker_color="#900C3F",
                ),
                go.Bar(
                    name="Important",
                    x=CSlitigateact2_labels,
                    y=CSlitigateact2_important,
                    marker_color="#C70039",
                ),
                go.Bar(
                    name="Slightly important",
                    x=CSlitigateact2_labels,
                    y=CSlitigateact2_slightly_important,
                    marker_color="#FF5733",
                ),
                go.Bar(
                    name="Not important at all",
                    x=CSlitigateact2_labels,
                    y=CSlitigateact2_not_important,
                    marker_color="#FFC300",
                ),
            ],
        )
    )

    campact2other_list = df[filter]["CSlitigateact2other"].dropna().to_list()
    st.write("### If you selected ‘other’, please specify `[CSlitigateact2other]`")
    if len(campact2other_list) > 0:
        for i in campact2other_list:
            if type(i) != float:
                st.write("- " + i)
    else:
        st.write("_no answers given_")

    st.write("## Costs")

    st.write(
        "### How frequently did the costs (e.g. court fees, loser pays principles, lawyers fees) prevent your organisation from starting a strategic litigation process? `[CSlitigatecost1]`"
    )
    CSlitigatecost1_counts = df[filter]["CSlitigatecost1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSlitigatecost1_counts,
            names=CSlitigatecost1_counts.index,
            color=CSlitigatecost1_counts.index,
            color_discrete_map={
                "Always or very often": px.colors.qualitative.Prism[9],
                "Often (75% of the time)": px.colors.qualitative.Prism[8],
                "Sometimes (50% of the time)": px.colors.qualitative.Prism[7],
                "Rarely (25% of the time)": px.colors.qualitative.Prism[6],
                "Never or rarely": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write(
        "### How frequently did your organisation benefit from pro bono support? `[CSlitigatecost2]`"
    )
    CSlitigatecost2_counts = df[filter]["CSlitigatecost2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSlitigatecost2_counts,
            names=CSlitigatecost2_counts.index,
            color=CSlitigatecost2_counts.index,
            color_discrete_map={
                "Always or very often": px.colors.qualitative.Prism[9],
                "Often (75% of the time)": px.colors.qualitative.Prism[8],
                "Sometimes (50% of the time)": px.colors.qualitative.Prism[7],
                "Rarely (25% of the time)": px.colors.qualitative.Prism[6],
                "Never or rarely": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write(
        "### Imagine your organisation lost a strategic litigation case concerning surveillance by intelligence agencies. How financially risky would it be for the organisation to be defeated in court? `[CSlitigatecost3]`"
    )
    CSlitigatecost3_counts = df[filter]["CSlitigatecost3"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSlitigatecost3_counts,
            names=CSlitigatecost3_counts.index,
            color=CSlitigatecost3_counts.index,
            color_discrete_map={
                "Not risky at all": px.colors.qualitative.Prism[9],
                "Somewhat risky": px.colors.qualitative.Prism[8],
                "Very risky": px.colors.qualitative.Prism[7],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write("## Transnational Scope")

    st.write(
        "### How frequently do your strategic litigation cases address transnational issues of surveillance by intelligence agencies? `[CSlitigatetrans1]`"
    )
    CSlitigatetrans1_counts = df[filter]["CSlitigatetrans1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSlitigatetrans1_counts,
            names=CSlitigatetrans1_counts.index,
            color=CSlitigatetrans1_counts.index,
            color_discrete_map={
                "Always": px.colors.qualitative.Prism[9],
                "Often (75% of the time)": px.colors.qualitative.Prism[8],
                "Sometimes (50% of the time)": px.colors.qualitative.Prism[7],
                "Rarely (25% of the time)": px.colors.qualitative.Prism[6],
                "Never": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write(
        "### When performing strategic litigation concerning surveillance by intelligence agencies, how often do you collaborate with civil society actors in other countries? `[CSlitigatetrans2]`"
    )
    CSlitigatetrans2_counts = df[filter]["CSlitigatetrans2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSlitigatetrans2_counts,
            names=CSlitigatetrans2_counts.index,
            color=CSlitigatetrans2_counts.index,
            color_discrete_map={
                "Always": px.colors.qualitative.Prism[9],
                "Often (75% of the time)": px.colors.qualitative.Prism[8],
                "Sometimes (50% of the time)": px.colors.qualitative.Prism[7],
                "Rarely (25% of the time)": px.colors.qualitative.Prism[6],
                "Never": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write("## Perceived Impact")

    st.write(
        "### How much do you agree with the following statements concerning the effectiveness of your strategic litigation activities regarding surveillance by intelligence agencies over the past 5 years? `[CSlitigateimpact1]`"
    )
    CSlitigateimpact1_labels = [
        "Helped increase public awareness",
        "Changed the prevalent case law",
        "Led to amendments in legislation",
        "Revealed new information",
        "Achieved defined goals",
    ]
    CSlitigateimpact1_agree_completely = []
    CSlitigateimpact1_agree_to_great_extent = []
    CSlitigateimpact1_agree_somewhat = []
    CSlitigateimpact1_agree_slightly = []
    CSlitigateimpact1_not_agree_at_all = []
    for agreement in [
        "Agree completely",
        "Agree to a great extent",
        "Agree somewhat",
        "Agree slightly",
        "Not agree at all",
    ]:
        for label in CSlitigateimpact1_options:
            try:
                count = df[filter][f"CSlitigateimpact1[{label}]"].value_counts()[
                    agreement
                ]
            except KeyError:
                count = 0
            if agreement == "Agree completely":
                CSlitigateimpact1_agree_completely.append(count)
            elif agreement == "Agree to a great extent":
                CSlitigateimpact1_agree_to_great_extent.append(count)
            elif agreement == "Agree somewhat":
                CSlitigateimpact1_agree_somewhat.append(count)
            elif agreement == "Agree slightly":
                CSlitigateimpact1_agree_slightly.append(count)
            elif agreement == "Not agree at all":
                CSlitigateimpact1_not_agree_at_all.append(count)
            else:
                continue
    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Agree completely",
                    x=CSlitigateimpact1_labels,
                    y=CSlitigateimpact1_agree_completely,
                    marker_color="#581845",
                ),
                go.Bar(
                    name="Agree to a great extent",
                    x=CSlitigateimpact1_labels,
                    y=CSlitigateimpact1_agree_to_great_extent,
                    marker_color="#900C3F",
                ),
                go.Bar(
                    name="Agree somewhat",
                    x=CSlitigateimpact1_labels,
                    y=CSlitigateimpact1_agree_somewhat,
                    marker_color="#C70039",
                ),
                go.Bar(
                    name="Agree slightly",
                    x=CSlitigateimpact1_labels,
                    y=CSlitigateimpact1_agree_slightly,
                    marker_color="#FF5733",
                ),
                go.Bar(
                    name="Not agree at all",
                    x=CSlitigateimpact1_labels,
                    y=CSlitigateimpact1_not_agree_at_all,
                    marker_color="#FFC300",
                ),
            ],
        )
    )

    CSlitigateimpact2_list = df[filter]["CSlitigateimpact2"].dropna().to_list()
    st.write(
        "### Please give an example for the impact that you see, such as references to your lawsuits or complaints, personal feedback you received, etc. `[CSlitigateimpact2]`"
    )
    if len(CSlitigateimpact2_list) > 0:
        for i in CSlitigateimpact2_list:
            if type(i) != float:
                st.write("- " + i.replace("\n", " "))
    else:
        st.write("_no answers given_")


if selected_section == "Protection":

    st.write("# Protection")

    st.write("## Operational Protection")

    st.write(
        "### Have you taken any of the following measures to protect your datas from attacks and surveillance? `[CSprotectops1]`"
    )
    CSprotectops1_options = [
        "Participation in digital security training",
        "Use of E2E encrypted communication channels",
    ]

    CSprotectops1_yes = []
    CSprotectops1_no = []
    CSprotectops1_dont_know = []
    CSprotectops1_prefer_not_to_say = []
    for answer in [
        "Yes",
        "No",
        "I don't know",
        "I prefer not to say",
    ]:
        for label in ["sectraining", "e2e"]:
            try:
                count = df[filter][f"CSprotectops1[{label}]"].value_counts()[answer]
            except KeyError:
                count = 0
            if answer == "Yes":
                CSprotectops1_yes.append(count)
            elif answer == "No":
                CSprotectops1_no.append(count)
            elif answer == "I don't know":
                CSprotectops1_dont_know.append(count)
            elif answer == "I prefer not to say":
                CSprotectops1_prefer_not_to_say.append(count)
            else:
                continue

    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=CSprotectops1_options,
                    y=CSprotectops1_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=CSprotectops1_options,
                    y=CSprotectops1_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=CSprotectops1_options,
                    y=CSprotectops1_dont_know,
                    marker_color=px.colors.qualitative.Prism[10],
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=CSprotectops1_options,
                    y=CSprotectops1_prefer_not_to_say,
                    marker_color=px.colors.qualitative.Prism[10],
                ),
            ],
        )
    )

    st.write(
        "### Were any of these measures provided by your employer? `[CSprotectops2]`"
    )
    CSprotectops2_counts = df[filter]["CSprotectops2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSprotectops2_counts,
            names=CSprotectops2_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
        )
    )

    st.write(
        "### How important is the use of the following technical tools for you to protect your communications, your online activities and the data you handle? `[CSprotectops3]`"
    )
    CSprotectops3_options = [
        "Encrypted Email",
        "VPN",
        "Tor",
        "E2E Messengers",
        "Encrpyted hardware",
        "Two-Factor authentication",
        "Other",
    ]

    CSprotectops3_very_important = []
    CSprotectops3_somewhat_important = []
    CSprotectops3_important = []
    CSprotectops3_slightly_important = []
    CSprotectops3_not_important = []
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
                count = df[filter][f"CSprotectops3[{label}]"].value_counts()[importance]
            except KeyError:
                count = 0
            if importance == "Very important":
                CSprotectops3_very_important.append(count)
            elif importance == "Somewhat important":
                CSprotectops3_somewhat_important.append(count)
            elif importance == "Important":
                CSprotectops3_important.append(count)
            elif importance == "Slightly important":
                CSprotectops3_slightly_important.append(count)
            elif importance == "Not important at all":
                CSprotectops3_not_important.append(count)
            else:
                continue

    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Very important",
                    x=CSprotectops3_options,
                    y=CSprotectops3_very_important,
                    marker_color="#581845",
                ),
                go.Bar(
                    name="Somewhat important",
                    x=CSprotectops3_options,
                    y=CSprotectops3_somewhat_important,
                    marker_color="#900C3F",
                ),
                go.Bar(
                    name="Important",
                    x=CSprotectops3_options,
                    y=CSprotectops3_important,
                    marker_color="#C70039",
                ),
                go.Bar(
                    name="Slightly important",
                    x=CSprotectops3_options,
                    y=CSprotectops3_slightly_important,
                    marker_color="#FF5733",
                ),
                go.Bar(
                    name="Not important at all",
                    x=CSprotectops3_options,
                    y=CSprotectops3_not_important,
                    marker_color="#FFC300",
                ),
            ],
        )
    )

    CSprotectops3other_list = df[filter]["CSprotectops3other"].dropna().to_list()
    st.write("### If you selected ‘other’, please specify `[CSprotectops3other]`")
    if len(CSprotectops3other_list) > 0:
        for i in CSprotectops3other_list:
            if type(i) != float:
                st.write("- " + i)
    else:
        st.write("_no answers given_")

    st.write(
        "### Which of the following statements best describes your level of confidence in the protection offered by technological tools? `[CSprotectops4]`"
    )
    CSprotectops4_counts = df[filter]["CSprotectops4"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            CSprotectops4_counts,
            values=CSprotectops4_counts,
            names=CSprotectops4_counts.index,
            color=CSprotectops4_counts.index,
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

    # TODO Clarify that in MS it's about source CSprotection (also for CSprotectleg2)
    st.write(
        "### When working on intelligence-related issues, do you feel you have reason to be concerned about surveillance of your activities `[CSprotectleg1]`"
    )

    CSprotectleg1_counts = df[filter]["CSprotectleg1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSprotectleg1_counts,
            names=CSprotectleg1_counts.index,
            color=CSprotectleg1_counts.index,
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
        "### Do you regard the existing legal CSprotections against surveillance of your activities in your country as a sufficient safeguard for your work on intelligence-related issues? `[CSprotectleg2]`"
    )

    CSprotectleg2_counts = df[filter]["CSprotectleg2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            CSprotectleg2_counts,
            values=CSprotectleg2_counts,
            names=CSprotectleg2_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
            color=CSprotectleg2_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write("### If you selected ‘no’, please specify `[CSprotectleg2no]`")
    for i in df[filter]["CSprotectleg2no"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write(
        "### Are any of the following forms of institutional support readily available to you? `[CSprotectleg3]`"
    )
    CSprotectleg3_options = ["Free legal counsel", "Legal cost insurance", "Other"]
    CSprotectleg3_yes = []
    CSprotectleg3_no = []
    CSprotectleg3_dont_know = []
    CSprotectleg3_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in ["free_counsel", "cost_insurance", "other"]:
            try:
                count = df[filter][f"CSprotectleg3[{label}]"].value_counts()[answer]
            except KeyError:
                count = 0
            if answer == "Yes":
                CSprotectleg3_yes.append(count)
            elif answer == "No":
                CSprotectleg3_no.append(count)
            elif answer == "I don't know":
                CSprotectleg3_dont_know.append(count)
            elif answer == "I prefer not to say":
                CSprotectleg3_prefer_not_to_say.append(count)
            else:
                continue
    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=CSprotectleg3_options,
                    y=CSprotectleg3_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=CSprotectleg3_options,
                    y=CSprotectleg3_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=CSprotectleg3_options,
                    y=CSprotectleg3_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=CSprotectleg3_options,
                    y=CSprotectleg3_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        )
    )

    protectleg3other_list = df[filter]["CSprotectleg3other"].dropna().to_list()
    st.write("### If you selected ‘other’, please specify `[CSprotectleg3other]`")
    if len(protectleg3other_list) > 0:
        for i in protectleg3other_list:
            if type(i) != float:
                st.write("- " + i)
    else:
        st.write("_no answers given_")

if selected_section == "Constraints":

    st.write("# Constraints")

    st.write("## Interference by state authorities")

    st.write(
        "### Has your institution or have you yourself been subjected to surveillance by intelligence agencies in the past five years? `[CSconstraintinter1]`"
    )

    CSconstraintinter1_counts = df[filter]["CSconstraintinter1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSconstraintinter1_counts,
            names=CSconstraintinter1_counts.index,
            color=CSconstraintinter1_counts.index,
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
        "### In the past 5 years, have you been threatened with prosecution or have you actually been prosecuted for your work on intelligence-related issues? `[CSconstraintinter2]`"
    )

    CSconstraintinter2_counts = df[filter]["CSconstraintinter2"].value_counts()
    CSconstraintinter2_fig = px.pie(
        df[filter],
        values=CSconstraintinter2_counts,
        names=CSconstraintinter2_counts.index,
        color_discrete_sequence=px.colors.qualitative.Prism,
    )

    st.plotly_chart(CSconstraintinter2_fig)

    st.write("### What was the outcome? `[CSconstraintinter3]`")

    CSconstraintinter3_counts = df[filter]["CSconstraintinter3"].value_counts()
    if len(CSconstraintinter3_counts) > 0:
        st.plotly_chart(
            render_pie_chart(
                df[filter],
                values=CSconstraintinter3_counts,
                names=CSconstraintinter3_counts.index,
                color_discrete_sequence=px.colors.qualitative.Prism,
            )
        )
    else:
        st.write("_no answers given_")

    st.write(
        "### In the past 5 years, have you experienced any of the following interferences by public authorities in relation to your work on intelligence related topics? `[CSconstraintinter4]`"
    )
    # TODO Map proper labels
    CSconstraintinter4_yes = []
    CSconstraintinter4_no = []
    CSconstraintinter4_dont_know = []
    CSconstraintinter4_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in CSconstraintinter4_options:
            try:
                count = df[filter][f"CSconstraintinter4[{label}]"].value_counts()[
                    answer
                ]
            except KeyError:
                count = 0
            if answer == "Yes":
                CSconstraintinter4_yes.append(count)
            elif answer == "No":
                CSconstraintinter4_no.append(count)
            elif answer == "I don't know":
                CSconstraintinter4_dont_know.append(count)
            elif answer == "I prefer not to say":
                CSconstraintinter4_prefer_not_to_say.append(count)
            else:
                continue
    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=CSconstraintinter4_options,
                    y=CSconstraintinter4_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=CSconstraintinter4_options,
                    y=CSconstraintinter4_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=CSconstraintinter4_options,
                    y=CSconstraintinter4_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=CSconstraintinter4_options,
                    y=CSconstraintinter4_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        )
    )

    st.write(
        "### In the past 5 years, have you been approached by intelligence officials and received... `[CSconstraintinter5]`"
    )
    CSconstraintinter5_options = [
        "Unsolicited information",
        "Invitations to off-the-record events or meetings",
        "Other",
    ]
    CSconstraintinter5_yes = []
    CSconstraintinter5_no = []
    CSconstraintinter5_dont_know = []
    CSconstraintinter5_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in ["unsolicited_information", "invitations", "other"]:
            try:
                count = df[filter][f"CSconstraintinter5[{label}]"].value_counts()[
                    answer
                ]
            except KeyError:
                count = 0
            if answer == "Yes":
                CSconstraintinter5_yes.append(count)
            elif answer == "No":
                CSconstraintinter5_no.append(count)
            elif answer == "I don't know":
                CSconstraintinter5_dont_know.append(count)
            elif answer == "I prefer not to say":
                CSconstraintinter5_prefer_not_to_say.append(count)
            else:
                continue
    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=CSconstraintinter5_options,
                    y=CSconstraintinter5_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=CSconstraintinter5_options,
                    y=CSconstraintinter5_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=CSconstraintinter5_options,
                    y=CSconstraintinter5_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=CSconstraintinter5_options,
                    y=CSconstraintinter5_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        )
    )

    constraintinter5other_list = (
        df[filter]["CSconstraintinter5other"].dropna().to_list()
    )
    st.write("### If you selected ‘other’, please specify `[CSconstraintinter5other]`")
    if len(constraintinter5other_list) > 0:
        for i in constraintinter5other_list:
            if type(i) != float:
                st.write("- " + i)
    else:
        st.write("_no answers given_")

    st.write(
        "### When working on intelligence-related issues have you ever experienced harassment by security agencies or politicians due to your... `[CSconstraintinter6]`"
    )
    CSconstraintinter6_options = [
        "Gender",
        "Ethnicity",
        "Political orientation",
        "Sexual orientation",
        "Religious affiliation",
        "Other",
    ]
    CSconstraintinter6_yes = []
    CSconstraintinter6_no = []
    CSconstraintinter6_dont_know = []
    CSconstraintinter6_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in [
            "gender",
            "ethnicity",
            "political",
            "sexual",
            "religious",
            "other",
        ]:
            try:
                count = df[filter][f"CSconstraintinter6[{label}]"].value_counts()[
                    answer
                ]
            except KeyError:
                count = 0
            if answer == "Yes":
                CSconstraintinter6_yes.append(count)
            elif answer == "No":
                CSconstraintinter6_no.append(count)
            elif answer == "I don't know":
                CSconstraintinter6_dont_know.append(count)
            elif answer == "I prefer not to say":
                CSconstraintinter6_prefer_not_to_say.append(count)
            else:
                continue
    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=CSconstraintinter6_options,
                    y=CSconstraintinter6_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=CSconstraintinter6_options,
                    y=CSconstraintinter6_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=CSconstraintinter6_options,
                    y=CSconstraintinter6_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=CSconstraintinter6_options,
                    y=CSconstraintinter6_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        )
    )

    constraintinter6other_list = (
        df[filter]["CSconstraintinter6other"].dropna().to_list()
    )
    st.write("### If you selected ‘other’, please specify `[CSconstraintinter6other]`")
    if len(constraintinter6other_list) > 0:
        for i in constraintinter6other_list:
            if type(i) != float:
                st.write("- " + i)
    else:
        st.write("_no answers given_")

    st.write("## Self-Censorship")

    st.write(
        "### Which of the following behaviours have you experienced or observed in your professional environment related to your work on intelligence-related topics? `[CSconstraintself1]`"
    )
    CSconstraintself1_labels = [
        "Avoided advocating for contentious policy changes",
        "Canceled a public campaign",
        "Withdrew litigation case",
        "Quit working on intelligence-related issues",
        "Other",
    ]
    CSconstraintself1_yes = []
    CSconstraintself1_no = []
    CSconstraintself1_dont_know = []
    CSconstraintself1_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in CSconstraintself1_options:
            try:
                count = df[filter][f"CSconstraintself1[{label}]"].value_counts()[answer]
            except KeyError:
                count = 0
            if answer == "Yes":
                CSconstraintself1_yes.append(count)
            elif answer == "No":
                CSconstraintself1_no.append(count)
            elif answer == "I don't know":
                CSconstraintself1_dont_know.append(count)
            elif answer == "I prefer not to say":
                CSconstraintself1_prefer_not_to_say.append(count)
            else:
                continue
    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=CSconstraintself1_labels,
                    y=CSconstraintself1_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=CSconstraintself1_labels,
                    y=CSconstraintself1_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=CSconstraintself1_labels,
                    y=CSconstraintself1_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=CSconstraintself1_labels,
                    y=CSconstraintself1_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        )
    )

    constraintself1other_list = df[filter]["CSconstraintself1other"].dropna().to_list()
    st.write("### If you selected ‘other’, please specify `[CSconstraintself1other]`")
    if len(constraintself1other_list) > 0:
        for i in constraintself1other_list:
            if type(i) != float:
                st.write("- " + i)
    else:
        st.write("_no answers given_")

if selected_section == "Attitudes":

    st.write("# CSattitudes")

    st.write(
        "### The following four statements are about **intelligence agencies**. Please select the statement you most agree with, based on your national context. `[CSattitude1]`"
    )

    CSattitude1_counts = df[filter]["CSattitude1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSattitude1_counts,
            names=CSattitude1_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
        )
    )

    # Pie chart CSattitudes (CSattitude2)
    st.write(
        "### The following four statements are about **intelligence oversight**. Please select the statement you most agree with, based on your national context. `[CSattitude2]`"
    )

    CSattitude2_counts = df[filter]["CSattitude2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=CSattitude2_counts,
            names=CSattitude2_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
        )
    )

    # Histogram (CSattitude3)

    st.write(
        "### In your personal view, what are the goals of intelligence oversight? Please select the three goals of oversight you subscribe to the most. `[CSattitude3]`"
    )

    # TODO Map proper labels
    CSattitude3_options = [
        "rule_of_law",
        "civil_liberties",
        "effectiveness_of_intel",
        "legitimacy_of_intel",
        "trust_in_intel",
        "critique_of_intel",
        "prefer_not_to_say",
    ]

    CSattitude3_df = pd.DataFrame(columns=("option", "count", "country"))
    for label in CSattitude3_options:
        CSattitude3_data = df[filter]["country"][
            df[f"CSattitude3[{label}]"] == 1
        ].tolist()
        for i in CSattitude3_data:
            CSattitude3_df = CSattitude3_df.append(
                {"option": label, "count": CSattitude3_data.count(i), "country": i},
                ignore_index=True,
            )
    CSattitude3_df = CSattitude3_df.drop_duplicates()

    st.plotly_chart(
        generate_histogram(
            df=CSattitude3_df,
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
        "The media",
    ]

    st.write(
        "### Which of the following actors do you trust the most to **enable public debate** on surveillance by intelligence agencies? `[CSattitude4]`"
    )
    st.plotly_chart(render_ranking_plot("CSattitude4"))

    st.write(
        "### Which of the following actors do you trust the most to **contest surveillance** by intelligence agencies? `[CSattitude5]`"
    )
    st.plotly_chart(render_ranking_plot("CSattitude5"))

    st.write(
        "### Which of the following actors do you trust the most to **enforce compliance** regarding surveillance by intelligence agencies? `[CSattitude6]`"
    )
    st.plotly_chart(render_ranking_plot("CSattitude6"))

if selected_section == "Appendix":
    st.write("# Appendix")

    st.write("## Raw data")

    st.write(get_csv_download_link(df, "civsoc"), unsafe_allow_html=True)
    st.write(get_excel_download_link(df, "civsoc"), unsafe_allow_html=True)

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

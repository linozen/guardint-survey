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
    color_discrete_map=None,
    hover_data=None,
    custom_data=None,
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


###################################################################################
# General configuration
###################################################################################


st.set_page_config(
    page_title="IOI Survey Data Explorer | Media",
)


###############################################################################
# Data wrangling
###############################################################################


@st.cache()
def get_ms_df():
    # Merge CSV files into DataFrame
    ms_csv_files = [
        "data/ms_uk_short.csv",
        "data/ms_de_short.csv",
        "data/ms_fr_short.csv",
    ]
    df_list = []
    for csv in ms_csv_files:
        df_list.append(pd.read_csv(csv, sep=";"))
    df = pd.concat(df_list, ignore_index=True)

    # Rename columns
    df = df.rename(
        columns={
            "startlanguage": "country",
            "lastpage": "lastpage",
            "MFfoi2": "MSfoi2",
            "MShr3[SQ01]": "MShr3[daily_newspaper]",
            "MShr3[SQ02]": "MShr3[weekly_newspaper]",
            "MShr3[SQ03]": "MShr3[magazine]",
            "MShr3[SQ04]": "MShr3[tv]",
            "MShr3[SQ05]": "MShr3[radio]",
            "MShr3[SQ06]": "MShr3[news_agency]",
            "MShr3[SQ07]": "MShr3[online_stand_alone]",
            "MShr3[SQ08]": "MShr3[online_of_offline]",
            "MSfoi5[SQ01]": "MSfoi5[not_aware]",
            "MSfoi5[SQ02]": "MSfoi5[not_covered]",
            "MSfoi5[SQ03]": "MSfoi5[too_expensive]",
            "MSfoi5[SQ04]": "MSfoi5[too_time_consuming]",
            "MSfoi5[SQ05]": "MSfoi5[afraid_of_data_destruction]",
            "MSfoi5[SQ06]": "MSfoi5[afraid_of_discrimination]",
            "MSfoi5[SQ07]": "MSfoi5[other]",
            "MSfoi5specify": "MSfoi5other",
            "MSfoi5[SQ08]": "MSfoi5[dont_know]",
            "MSfoi5[SQ09]": "MSfoi5[prefer_not_to_say]",
            "MSsoc5[SQ01]": "MSsoc5[follow_up_on_other_media]",
            "MSsoc5[SQ02]": "MSsoc5[statements_government]",
            "MSsoc5[SQ03]": "MSsoc5[oversight_reports]",
            "MSsoc5[SQ04]": "MSsoc5[leaks]",
            "MSsoc5[SQ05]": "MSsoc5[own_investigations]",
            "MSsoc5[SQ07]": "MSsoc5[dont_know]",
            "MSsoc5[SQ08]": "MSsoc5[prefer_not_to_say]",
            "MSsoc5[SQ09]": "MSsoc5[other]",
            "MSsoc6[SQ01]": "MSsoc6[national_security_risks]",
            "MSsoc6[SQ02]": "MSsoc6[intelligence_success]",
            "MSsoc6[SQ03]": "MSsoc6[intelligence_misconduct]",
            "MSsoc6[SQ04]": "MSsoc6[oversight_interventions]",
            "MSsoc6[SQ05]": "MSsoc6[oversight_failures]",
            "MSsoc6[SQ06]": "MSsoc6[policy_debates_leg_reforms]",
            "MSsoc6[SQ07]": "MSsoc6[other]",
            "MSimpact1[SQ01]": "MSimpact1[above_avg_comments]",
            "MSimpact1[SQ02]": "MSimpact1[above_avg_shares]",
            "MSimpact1[SQ03]": "MSimpact1[above_avg_readers]",
            "MSimpact1[SQ04]": "MSimpact1[letters_to_the_editor]",
            "MSimpact1[SQ05]": "MSimpact1[follow_up_by_other_media]",
            "MSimpact1[SQ06]": "MSimpact1[other]",
            "MSimpact1[SQ07]": "MSimpact1[none_of_the_above]",
            "MSimpact1[SQ08]": "MSimpact1[dont_know]",
            "MSimpact1[SQ09]": "MSimpact1[prefer_not_to_say]",
            "MSimpact2[SQ01]": "MSimpact2[diplomatic_pressure]",
            "MSimpact2[SQ02]": "MSimpact2[civic_action]",
            "MSimpact2[SQ03]": "MSimpact2[conversations_with_government]",
            "MSimpact2[SQ04]": "MSimpact2[official_inquiries]",
            "MSimpact2[SQ05]": "MSimpact2[government_statements]",
            "MSimpact2[SQ06]": "MSimpact2[conversations_with_intelligence]",
            "MSimpact2[SQ08]": "MSimpact2[dont_know]",
            "MSimpact2[SQ09]": "MSimpact2[prefer_not_to_say]",
            "MSimpact2[SQ10]": "MSimpact2[other]",
            "MSimpact2[SQ11]": "MSimpact2[none_of_the_above]",
            "MSprotectops1[SQ01]": "MSprotectops1[sectraining]",
            "MSprotectops1[SQ02]": "MSprotectops1[secure_drop]",
            "MSprotectops1[SQ03]": "MSprotectops1[e2e]",
            "MSprotectops3[SQ01]": "MSprotectops3[encrypted_email]",
            "MSprotectops3[SQ02]": "MSprotectops3[vpn]",
            "MSprotectops3[SQ03]": "MSprotectops3[tor]",
            "MSprotectops3[SQ04]": "MSprotectops3[e2e_chat]",
            "MSprotectops3[SQ05]": "MSprotectops3[encrypted_hardware]",
            "MSprotectops3[SQ06]": "MSprotectops3[2fa]",
            "MSprotectops3[SQ07]": "MSprotectops3[secure_drop]",
            "MSprotectops3[SQ08]": "MSprotectops3[other]",
            "MSprotectleg2A": "MSprotectleg2",
            "MSprotectleg3[SQ01]": "MSprotectleg3[free_counsel]",
            "MSprotectleg3[SQ02]": "MSprotectleg3[cost_insurance]",
            "MSprotectleg3[SQ03]": "MSprotectleg3[other]",
            "MSprotectleg4[SQ01]": "MSprotectleg4[free_counsel]",
            "MSprotectleg4[SQ02]": "MSprotectleg4[cost_insurance]",
            "MSprotectleg4[SQ03]": "MSprotectleg4[other]",
            "MScontstraintinter1": "MSconstraintinter1",
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
            "MSconstraintinter5ot": "MSconstraintinter5other",
            "MSconstraintinter6[SQ01]": "MSconstraintinter6[gender]",
            "MSconstraintinter6[SQ02]": "MSconstraintinter6[ethnicity]",
            "MSconstraintinter6[SQ03]": "MSconstraintinter6[political]",
            "MSconstraintinter6[SQ04]": "MSconstraintinter6[sexual]",
            "MSconstraintinter6[SQ05]": "MSconstraintinter6[religious]",
            "MSconstraintinter6[SQ06]": "MSconstraintinter6[other]",
            "MSconstraintinter6ot": "MSconstraintinter6other",
            "MSconstraintself1[SQ01]": "MSconstraintself1[avoid]",
            "MSconstraintself1[SQ02]": "MSconstraintself1[change_focus]",
            "MSconstraintself1[SQ03]": "MSconstraintself1[change_timeline]",
            "MSconstraintself1[SQ04]": "MSconstraintself1[abandon]",
            "MSconstraintself1[SQ05]": "MSconstraintself1[leave_profession]",
            "MSconstraintself1[SQ06]": "MSconstraintself1[other]",
            "MSconstraintself1ot": "MSconstraintself1other",
            "MSattitude3[SQ01]": "MSattitude3[rule_of_law]",
            "MSattitude3[SQ02]": "MSattitude3[civil_liberties]",
            "MSattitude3[SQ03]": "MSattitude3[effectiveness_of_intel]",
            "MSattitude3[SQ04]": "MSattitude3[legitimacy_of_intel]",
            "MSattitude3[SQ05]": "MSattitude3[trust_in_intel]",
            "MSattitude3[SQ06]": "MSattitude3[critique_of_intel]",
            "MSattitude3[SQ07]": "MSattitude3[prefer_not_to_say]",
            "MSgendersd": "MSgenderother",
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
            "MShr1",
            "MShr2",
            "MShr3[daily_newspaper]",
            "MShr3[weekly_newspaper]",
            "MShr3[magazine]",
            "MShr3[tv]",
            "MShr3[radio]",
            "MShr3[news_agency]",
            "MShr3[online_stand_alone]",
            "MShr3[online_of_offline]",
            "MShr4",
            "MSexpertise1",
            "MSexpertise2",
            "MSexpertise3",
            "MSexpertise4",
            "MSfinance1",
            "MSfinance2",
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
            "MSfoi5[other]",
            "MSfoi5other",
            "MSfoi5[dont_know]",
            "MSfoi5[prefer_not_to_say]",
            "MSapp1",
            "MSapp2",
            "MSsoc1",
            "MSsoc2",
            "MSsoc4",
            "MSsoc5[follow_up_on_other_media]",
            "MSsoc5[statements_government]",
            "MSsoc5[oversight_reports]",
            "MSsoc5[leaks]",
            "MSsoc5[own_investigations]",
            "MSsoc5[dont_know]",
            "MSsoc5[prefer_not_to_say]",
            "MSsoc5[other]",
            "MSsoc5other",
            "MSsoc6[national_security_risks]",
            "MSsoc6[intelligence_success]",
            "MSsoc6[intelligence_misconduct]",
            "MSsoc6[oversight_interventions]",
            "MSsoc6[oversight_failures]",
            "MSsoc6[policy_debates_leg_reforms]",
            "MSsoc6[other]",
            "MSsoc6other",
            "MStrans1",
            "MStrans2",
            "MStrans3",
            "MSimpact1[above_avg_comments]",
            "MSimpact1[above_avg_shares]",
            "MSimpact1[above_avg_readers]",
            "MSimpact1[letters_to_the_editor]",
            "MSimpact1[follow_up_by_other_media]",
            "MSimpact1[other]",
            "MSimpact1other",
            "MSimpact1[none_of_the_above]",
            "MSimpact1[dont_know]",
            "MSimpact1[prefer_not_to_say]",
            "MSimpact2[diplomatic_pressure]",
            "MSimpact2[civic_action]",
            "MSimpact2[conversations_with_government]",
            "MSimpact2[official_inquiries]",
            "MSimpact2[government_statements]",
            "MSimpact2[conversations_with_intelligence]",
            "MSimpact2[dont_know]",
            "MSimpact2[prefer_not_to_say]",
            "MSimpact2[other]",
            "MSimpact2other",
            "MSimpact2[none_of_the_above]",
            "MSprotectops1[sectraining]",
            "MSprotectops1[secure_drop]",
            "MSprotectops1[e2e]",
            "MSprotectops2",
            "MSprotectops3[encrypted_email]",
            "MSprotectops3[vpn]",
            "MSprotectops3[tor]",
            "MSprotectops3[e2e_chat]",
            "MSprotectops3[encrypted_hardware]",
            "MSprotectops3[2fa]",
            "MSprotectops3[secure_drop]",
            "MSprotectops3[other]",
            "MSprotectops3other",
            "MSprotectops4",
            "MSprotectleg1",
            "MSprotectleg2",
            "MSprotectleg3[free_counsel]",
            "MSprotectleg3[cost_insurance]",
            "MSprotectleg3[other]",
            "MSprotectleg3other",
            "MSprotectleg4[free_counsel]",
            "MSprotectleg4[cost_insurance]",
            "MSprotectleg4[other]",
            "MSprotectleg4other",
            "MSprotectleg5",
            "MSprotectrta1",
            "MSprotectrta2",
            "MSprotectrta3",
            "MSprotectrta4",
            "MSprotectrta5",
            "MSprotectrta6",
            "MSconstraintcen1",
            "MSconstraintcen2",
            "MSconstraintcen3",
            "MSconstraintcen4",
            "MSconstraintcen4spec",
            "MSconstraintcen5",
            "MSconstraintcen5spec",
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
            "MSconstraintinter5other",
            "MSconstraintinter6[gender]",
            "MSconstraintinter6[ethnicity]",
            "MSconstraintinter6[political]",
            "MSconstraintinter6[sexual]",
            "MSconstraintinter6[religious]",
            "MSconstraintinter6[other]",
            "MSconstraintinter6other",
            "MSconstraintself1[avoid]",
            "MSconstraintself1[change_focus]",
            "MSconstraintself1[change_timeline]",
            "MSconstraintself1[abandon]",
            "MSconstraintself1[leave_profession]",
            "MSconstraintself1[other]",
            "MSconstraintself1other",
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
            "MSgender",
        ]
    ]

    # Set surveytype
    df["surveytype"] = "Media Scrutiny"
    return df


###############################################################################
# Define base DataFrame
###############################################################################


df = get_ms_df()
df = df.reset_index(drop=True)


###############################################################################
# Make answers human-readable
###############################################################################


df["MShr1"] = df["MShr1"].replace(
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

df["MShr4"] = df["MShr4"].replace(
    {
        "AO01": "I had enough time",
        "AO02": "I had some time",
        "AO03": "I had very little time",
        "AO04": "I had no time",
        "AO05": "I don't know",
        "AO06": "I prefer not to say",
    }
)

df["MSexpertise2"] = df["MSexpertise2"].replace(
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

df["MSexpertise3"] = df["MSexpertise3"].replace(
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

df["MSexpertise4"] = df["MSexpertise4"].replace(
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

df["MSfinance1"] = df["MSfinance1"].replace(
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

df["MSfinance2"] = df["MSfinance2"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

df["MSfoi1"] = df["MSfoi1"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

df["MSfoi3"] = df["MSfoi3"].replace(
    {
        "AO01": "Yes, within 30 days",
        "AO02": "No, usually longer than 30 days",
        "AO03": "Never",
        "AO04": "I don't know",
        "AO05": "I prefer not to say",
    }
)

df["MSfoi4"] = df["MSfoi4"].replace(
    {
        "AO01": "Very helpful",
        "AO02": "Helpful in parts",
        "AO03": "Not helpful at all",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["MSapp1"] = df["MSapp1"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
    }
)

df["MSapp2"] = df["MSapp2"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
    }
)

df["MSsoc4"] = df["MSsoc4"].replace(
    {
        "AO01": "Very regularly",
        "AO02": "Regularly",
        "AO03": "Somewhat regularly",
        "AO04": "Sometimes",
        "AO05": "Rarely or never",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

df["MStrans1"] = df["MStrans1"].replace(
    {
        "AO001": "Always",
        "AO002": "Often (75% of the time)",
        "AO003": "Sometimes (50% of the time)",
        "AO004": "Rarely (25% of the time)",
        "AO005": "Never",
        "AO006": "I don't know",
        "AO007": "I prefer not to say",
    }
)

df["MStrans2"] = df["MStrans2"].replace(
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

df["MStrans3"] = df["MStrans3"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

for label in [
    "sectraining",
    "secure_drop",
    "e2e",
]:
    df[f"MSprotectops1[{label}]"] = df[f"MSprotectops1[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

df["MSprotectops2"] = df["MSprotectops2"].replace(
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
    "secure_drop",
    "other",
]:
    df[f"MSprotectops3[{label}]"] = df[f"MSprotectops3[{label}]"].replace(
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


df["MSprotectops4"] = df["MSprotectops4"].replace(
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

df["MSprotectleg1"] = df["MSprotectleg1"].replace(
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

df["MSprotectleg2"] = df["MSprotectleg2"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

for label in ["free_counsel", "cost_insurance", "other"]:
    df[f"MSprotectleg3[{label}]"] = df[f"MSprotectleg3[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )
    df[f"MSprotectleg4[{label}]"] = df[f"MSprotectleg4[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

df["MSprotectleg5"] = df["MSprotectleg5"].replace(
    {
        "AO01": "Very common",
        "AO02": "Common",
        "AO03": "Somewhat common",
        "AO04": "Slightly common",
        "AO05": "Not common at all",
        "AO06": "I don't know",
        "AO07": "I prefer not to say",
    }
)

for i in range(1, 5):
    df[f"MSprotectrta{i}"] = df[f"MSprotectrta{i}"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

df["MSprotectrta5"] = df["MSprotectrta5"].replace(
    {
        "AO01": "Yes, within 30 days",
        "AO02": "No, usually longer than 30 days",
        "AO03": "Never",
        "AO04": "I don't know",
        "AO05": "I prefer not to say",
    }
)

df["MSprotectrta6"] = df["MSprotectrta6"].replace(
    {
        "AO01": "Yes, the information provided was helpful",
        "AO02": "Partly, the information provided was somewhat <br>helpful but contained omissions",
        "AO03": "No, the information provided was not at all helpful",
        "AO04": "I don't know",
        "AO05": "I prefer not to say",
    }
)

for i in [1, 2, 4, 5]:
    df[f"MSconstraintcen{i}"] = df[f"MSconstraintcen{i}"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

df["MSconstraintinter1"] = df["MSconstraintinter1"].replace(
    {
        "AO01": "Yes, I have evidence",
        "AO02": "Yes, I suspect",
        "AO03": "No",
        "AO04": "I don't know",
        "AO05": "I prefer not to say",
    }
)

df["MSconstraintinter2"] = df["MSconstraintinter2"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

df["MSconstraintinter3"] = df["MSconstraintinter3"].replace(
    {
        "AO01": "I was threatened with prosecution",
        "AO02": "I was prosecuted but acquitted",
        "AO03": "I was prosecuted and convicted",
        "AO04": "I don't know",
        "AO05": "I prefer not to say",
    }
)

MSconstraintinter4_options = [
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
for label in MSconstraintinter4_options:
    df[f"MSconstraintinter4[{label}]"] = df[f"MSconstraintinter4[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

MSconstraintinter5_options = ["unsolicited_information", "invitations", "other"]
for label in MSconstraintinter5_options:
    df[f"MSconstraintinter5[{label}]"] = df[f"MSconstraintinter5[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

MSconstraintinter6_options = [
    "gender",
    "ethnicity",
    "political",
    "sexual",
    "religious",
    "other",
]
for label in MSconstraintinter6_options:
    df[f"MSconstraintinter6[{label}]"] = df[f"MSconstraintinter6[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

MSconstraintself1_options = [
    "avoid",
    "change_focus",
    "change_timeline",
    "abandon",
    "leave_profession",
    "other",
]
for label in MSconstraintself1_options:
    df[f"MSconstraintself1[{label}]"] = df[f"MSconstraintself1[{label}]"].replace(
        {
            "AO01": "Yes",
            "AO02": "No",
            "AO03": "I don't know",
            "AO04": "I prefer not to say",
        }
    )

df["MSattitude1"] = df["MSattitude1"].replace(
    {
        "AO01": "Intelligence agencies are incompatible with democratic <br>values and should be abolished",
        "AO02": "Intelligence agencies contradict democratic principles,<br>and their powers should be kept at a bare minimum",
        "AO03": "Intelligence agencies are necessary and legitimate institutions <br>of democratic states, even though they may sometimes overstep <br>their legal mandates",
        "AO04": "Intelligence agencies are a vital component of national <br>security and should be shielded from excessive bureaucratic <br>restrictions",
        "AO05": "I prefer not to say",
    }
)

df["MSattitude2"] = df["MSattitude2"].replace(
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
        df[f"MSattitude{i}[{j}]"] = df[f"MSattitude{i}[{j}]"].replace(
            {
                "AO01": "Parliamentary oversight bodies",
                "AO02": "Judicial oversight bodies",
                "AO03": "Independent expert bodies",
                "AO04": "Data protection authorities",
                "AO05": "Audit courts",
                "AO06": "Civil society organisations",
            }
        )

df["MSgender"] = df["MSgender"].fillna("Not specified")
df["MSgender"] = df["MSgender"].replace(
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
df["MShr2"] = df["MShr2"].replace("?", np.nan)
df["MShr2"] = df["MShr2"].replace("0,5", 0.5)
df["MShr2"] = pd.to_numeric(df["MShr2"], errors="coerce")

df["MSexpertise1"] = df["MSexpertise1"].replace("?", np.nan)
df["MSexpertise1"] = df["MSexpertise1"].replace("<1", 0.5)
df["MSexpertise1"] = pd.to_numeric(df["MSexpertise1"], errors="coerce")

df["MSfoi2"] = df["MSfoi2"].replace(
    {"20+": 20.0, " ca 10": 10.0, "several": 3.0, "15+": 15.0}
)
df["MSfoi2"] = pd.to_numeric(df["MSfoi2"], errors="coerce")

df["MSsoc1"] = pd.to_numeric(df["MSsoc1"], errors="coerce")

df["MSsoc2"] = pd.to_numeric(df["MSsoc2"], errors="coerce")

# MSconstraintcen3 was marred by answers that didn't really answer the question.
# Below, I try to clean the responses as best as possible
df["MSconstraintcen3"] = df["MSconstraintcen3"].replace(
    {
        "10 fois.": 10.0,
    }
)
df["MSconstraintcen3"] = df["MSconstraintcen3"].replace(
    to_replace=r"^Maybe once or twice",
    value=2.0,
    regex=True,
)
# I removed this answer as it does not really answer the question
df["MSconstraintcen3"] = df["MSconstraintcen3"].replace(
    to_replace=r"^every time you publish a story you contact the subject",
    value=np.nan,
    regex=True,
)
df["MSconstraintcen3"] = df["MSconstraintcen3"].replace(
    to_replace=r"^moins de 5", value=4.0, regex=True
)
df["MSconstraintcen3"] = pd.to_numeric(df["MSconstraintcen3"], errors="coerce")

# Here, I change the datatype to boolean for all the multiple choice answers
for col in df:
    if (
        col.startswith("MShr3")
        or col.startswith("MSfoi5")
        or col.startswith("MSsoc5[")
        or col.startswith("MSsoc6[")
        or col.startswith("MSimpact1[")
        or col.startswith("MSimpact2[")
        or col.startswith("MSattitude3[")
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
    "Media Reporting",
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
    on_change=callback,
)

st.caption("__" + selected_section + "__ | Media representatives")

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


# df.to_pickle("./data/media.pkl")
# df.to_excel("./data/media.xlsx")
# df.to_csv("./data/media.csv")


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
    height=0,
)

st.markdown(
    """ <style> h3 {line-height: 1.3} </style> """,
    unsafe_allow_html=True,
)


###############################################################################
# Display dynamic charts
###############################################################################


if selected_section == "Overview":
    st.write("# Overview")

    merged_markdown = read_markdown_file("explorer/markdown/media.md")
    st.markdown(merged_markdown, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.metric("Media representatives", len(df[filter].index))
    col2.metric(
        "Cumulative years spent working on SBIA",
        df[filter]["MSexpertise1"].sum(),
    )

    col1, col2 = st.columns(2)
    col1.metric(
        "Average years spent working on SBIA???",
        "%.1f" % df[filter]["MSexpertise1"].mean(),
    )
    col2.metric(
        "Average Number of FOI requests sent in the past 5 years",
        int(df[filter]["MSfoi2"].mean()),
    )

    col1, col2 = st.columns(2)
    col1.metric(
        "Articles written on SBIA in the last year",
        "%.1f" % df[filter]["MSsoc2"].sum(),
    )
    col2.metric(
        "Average Articles written on SBIA in the last year",
        "%.1f" % df[filter]["MSsoc2"].mean(),
    )

    st.caption(
        "???For the calculation of the mean, only valid numerical answers were counted. This is why the number might differ from the number one gets when simply dividing e.g. the cumulative years spent working on SBIA by the overall number of respondents (including those who haven't specified their experience in years)."
    )

    st.write("### Country `[country]`")
    country_counts = df[filter]["country"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=country_counts,
            names=country_counts.index,
            color=country_counts.index,
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
        ),
        use_container_width=True,
    )

    st.write("### Gender `[MSgender]`")
    gender_counts = df[filter]["MSgender"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=gender_counts,
            names=gender_counts.index,
            color=gender_counts.index,
            color_discrete_map={
                "Not specified": px.colors.qualitative.Prism[10],
                "Male": px.colors.qualitative.Prism[9],
                "Female": px.colors.qualitative.Prism[7],
                "Other": px.colors.qualitative.Prism[5],
            },
        ),
        use_container_width=True,
    )
if selected_section == "Resources":
    st.write("# Resources")

    st.write("## Human Resources")

    st.write("### What is your employment status `[MShr1]`")
    MShr1_counts = df[filter]["MShr1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MShr1_counts,
            values=MShr1_counts,
            names=MShr1_counts.index,
            color=MShr1_counts.index,
            color_discrete_map={
                "Full-time": px.colors.qualitative.Prism[0],
                "Part-time (>50%)": px.colors.qualitative.Prism[1],
                "Part-time (<50%)": px.colors.qualitative.Prism[2],
                "Freelance": px.colors.qualitative.Prism[4],
                "Other": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### How many days per month do you work on surveillance by intelligence agencies? `[MShr2]`"
    )
    st.plotly_chart(
        render_histogram(
            df=df[filter],
            x="MShr2",
            y=None,
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"MShr2": "days per month"},
        ),
        use_container_width=True,
    )

    st.plotly_chart(
        render_boxplot(
            df=df[filter],
            points="all",
            x="country",
            y="MShr2",
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
        ),
        use_container_width=True,
    )

    st.write("### Which type of medium do you work for? `[MShr3]`")
    MShr3_df = pd.DataFrame(columns=("option", "count", "country"))
    # TODO Map proper labels
    for label in [
        "daily_newspaper",
        "weekly_newspaper",
        "magazine",
        "tv",
        "radio",
        "news_agency",
        "online_stand_alone",
        "online_of_offline",
    ]:
        MShr3_data = df[filter]["country"][df[f"MShr3[{label}]"] == 1].tolist()
        for i in MShr3_data:
            MShr3_df = MShr3_df.append(
                {"option": label, "count": MShr3_data.count(i), "country": i},
                ignore_index=True,
            )
    MShr3_df = MShr3_df.drop_duplicates()

    st.plotly_chart(
        render_histogram(
            MShr3_df,
            x="option",
            y="count",
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"count": "people who work for this medium"},
        ),
        use_container_width=True,
    )

    st.write(
        "### Within the past year, did you have enough time to cover surveillance by intelligence agencies? `[MShr4]`"
    )
    MShr4_counts = df[filter]["MShr4"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MShr4_counts,
            values=MShr4_counts,
            names=MShr4_counts.index,
            color=MShr4_counts.index,
            color_discrete_map={
                "I had enough time": px.colors.qualitative.Prism[9],
                "I had some time": px.colors.qualitative.Prism[8],
                "I had very little time": px.colors.qualitative.Prism[7],
                "I had no time": px.colors.qualitative.Prism[6],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("## Expertise")

    st.write(
        "### How many years have you spent working on surveillance by intelligence agencies? `[MSexpertise1]`"
    )
    st.plotly_chart(
        render_histogram(
            df[filter],
            x="MSexpertise1",
            y=None,
            nbins=20,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"MSexpertise1": "years"},
        ),
        use_container_width=True,
    )

    st.plotly_chart(
        render_boxplot(
            df=df[filter],
            points="all",
            x="country",
            y="MSexpertise1",
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### How do you assess your level of expertise concerning the **legal** aspects of surveillance by intelligence agencies???For example, knowledge of intelligence law, case law. `[MSexpertise2]`"
    )
    MSexpertise2_counts = df[filter]["MSexpertise2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=MSexpertise2_counts,
            names=MSexpertise2_counts.index,
            color_discrete_sequence=None,
            color=MSexpertise2_counts.index,
            color_discrete_map={
                "Expert knowledge": px.colors.qualitative.Prism[9],
                "Advanced knowledge": px.colors.qualitative.Prism[8],
                "Some knowledge": px.colors.qualitative.Prism[7],
                "Basic knowledge": px.colors.qualitative.Prism[6],
                "No knowledge": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### How do you assess your level of expertise concerning the **political** aspects of surveillance by intelligence agencies?` [MSexpertise3]`"
    )
    MSexpertise3_counts = df[filter]["MSexpertise3"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=MSexpertise3_counts,
            names=MSexpertise3_counts.index,
            color_discrete_sequence=None,
            color=MSexpertise3_counts.index,
            color_discrete_map={
                "Expert knowledge": px.colors.qualitative.Prism[9],
                "Advanced knowledge": px.colors.qualitative.Prism[8],
                "Some knowledge": px.colors.qualitative.Prism[7],
                "Basic knowledge": px.colors.qualitative.Prism[6],
                "No knowledge": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### How do you assess your level of expertise concerning the **technical** aspects of surveillance by intelligence agencies?` [MSexpertise4]`"
    )
    MSexpertise4_counts = df[filter]["MSexpertise4"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=MSexpertise4_counts,
            names=MSexpertise4_counts.index,
            color_discrete_sequence=None,
            color=MSexpertise4_counts.index,
            color_discrete_map={
                "Expert knowledge": px.colors.qualitative.Prism[9],
                "Advanced knowledge": px.colors.qualitative.Prism[8],
                "Some knowledge": px.colors.qualitative.Prism[7],
                "Basic knowledge": px.colors.qualitative.Prism[6],
                "No knowledge": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("## Financial Resources")

    st.write(
        "### How do you assess the financial resources that have been available for your work on intelligence over the past 5 years? `[MSfinance1]`"
    )
    MSfinance1_counts = df[filter]["MSfinance1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=MSfinance1_counts,
            names=MSfinance1_counts.index,
            color_discrete_sequence=None,
            color=MSfinance1_counts.index,
            color_discrete_map={
                "A great deal of funding": px.colors.qualitative.Prism[9],
                "Sufficient funding": px.colors.qualitative.Prism[8],
                "Some funding": px.colors.qualitative.Prism[7],
                "Little funding": px.colors.qualitative.Prism[6],
                "No funding": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### If you wanted to conduct investigative research into surveillance by intelligence agencies, could you access extra funding for this research? (For example, a special budget or a stipend) `[MSfinance2]`"
    )
    MSfinance2_counts = df[filter]["MSfinance2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSfinance2_counts,
            values=MSfinance2_counts,
            names=MSfinance2_counts.index,
            color=MSfinance2_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("## Freedom of Information")

    st.write(
        "### Have you requested information under the national Freedom of Information Law?? when you worked on intelligence-related issues over the past 5 years? `[MSfoi1]`"
    )
    MSfoi1_counts = df[filter]["MSfoi1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSfoi1_counts,
            values=MSfoi1_counts,
            names=MSfoi1_counts.index,
            color=MSfoi1_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("### How often did you request information? `[MSfoi2]`")
    st.plotly_chart(
        render_histogram(
            df[filter],
            x="MSfoi2",
            y=None,
            nbins=10,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"MSfoi2": "Number of requests"},
        ),
        use_container_width=True,
    )

    st.plotly_chart(
        render_boxplot(
            df=df[filter],
            points="all",
            x="country",
            y="MSfoi2",
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Over the past 5 years, did you receive a response to your FOI request(s) in a timely manner? `[MSfoi3]`"
    )
    MSfoi3_counts = df[filter]["MSfoi3"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSfoi3_counts,
            values=MSfoi3_counts,
            names=MSfoi3_counts.index,
            color=MSfoi3_counts.index,
            color_discrete_map={
                "Never": px.colors.qualitative.Prism[9],
                "No, usually longer than 30 days": px.colors.qualitative.Prism[8],
                "Yes, within 30 days": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### How helpful have FOI requests been for your work on intelligence-related issues? `[MSfoi4]`"
    )
    protectops2_counts = df[filter]["MSfoi4"].value_counts()

    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=protectops2_counts,
            names=protectops2_counts.index,
        ),
        use_container_width=True,
    )

    st.write(
        "### Why haven???t you requested information under the national FOI law when you reported on intelligence-related issues over the past 5 years? `[MSfoi5]`"
    )
    MSfoi5_df = pd.DataFrame(columns=("option", "count", "country"))
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
        MSfoi5_data = df[filter]["country"][df[f"MSfoi5[{label}]"] == 1].tolist()
        for i in MSfoi5_data:
            MSfoi5_df = MSfoi5_df.append(
                {"option": label, "count": MSfoi5_data.count(i), "country": i},
                ignore_index=True,
            )
    MSfoi5_df = MSfoi5_df.drop_duplicates()

    st.plotly_chart(
        render_histogram(
            MSfoi5_df,
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
        ),
        use_container_width=True,
    )

    st.write("## Appreciation")

    st.write(
        "### In the past 5 years, have stories on surveillance by intelligence agencies been nominated for a journalistic award in the country you primarily work in? `[MSapp1]`"
    )
    MSapp1_counts = df[filter]["MSapp1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSapp1_counts,
            values=MSapp1_counts,
            names=MSapp1_counts.index,
            color=MSapp1_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Are there specific awards in the country you primarily work in for reporting on intelligence-related topics? `[MSapp2]`"
    )
    MSapp2_counts = df[filter]["MSapp2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSapp2_counts,
            values=MSapp2_counts,
            names=MSapp2_counts.index,
            color=MSapp2_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

if selected_section == "Media Reporting":
    st.write("# Media Reporting")

    st.write("## Scope of Coverage")

    st.write(
        "### Please estimate: how many journalistic pieces have you produced on intelligence-related topics in the past year? `[MSsoc1]`"
    )
    st.plotly_chart(
        render_histogram(
            df=df[filter],
            x="MSsoc1",
            y=None,
            nbins=10,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"MSsoc1": "pieces produced lasy year"},
        ),
        use_container_width=True,
    )

    st.plotly_chart(
        render_boxplot(
            df=df[filter],
            points="all",
            x="country",
            y="MSsoc1",
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Please estimate: how many of these pieces focused on surveillance by intelligence agencies? `[MSsoc2]`"
    )
    st.plotly_chart(
        render_histogram(
            df=df[filter],
            x="MSsoc2",
            y=None,
            nbins=10,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={
                "MSsoc2": "pieces focused on surveillance by intelligence agencies"
            },
        ),
        use_container_width=True,
    )

    st.plotly_chart(
        render_boxplot(
            df=df[filter],
            points="all",
            x="country",
            y="MSsoc2",
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
        ),
        use_container_width=True,
    )

    MSsoc1_list = df[filter]["MSsoc1"].to_list()
    MSsoc2_list = df[filter]["MSsoc2"].to_list()

    st.write("### Comparison between `[MSsoc1]` and `[MSsoc2]`")
    st.plotly_chart(
        render_overlaid_histogram(
            traces=[MSsoc1_list, MSsoc2_list],
            names=[
                "all pieces on <br>intelligence",
                "pieces focused <br>on surveillance <br>by intelligence",
            ],
            colors=[px.colors.qualitative.Prism[0], px.colors.qualitative.Prism[2]],
        ),
        use_container_width=True,
    )

    df_comp = df[filter][["MSsoc1", "country"]].dropna()
    df_comp["subject"] = "all pieces on <br>intelligence"
    df_comp = df_comp.append(df[filter][["MSsoc2", "country"]].dropna())
    df_comp["subject"] = np.where(
        df_comp["MSsoc2"].notnull(),
        "pieces focused <br>on surveillance <br>by intelligence",
        "all pieces on <br>intelligence",
    )
    df_comp["pieces"] = df_comp.loc[:, ["MSsoc1", "MSsoc2"]].sum(axis=1)

    st.plotly_chart(
        render_boxplot(
            df=df_comp,
            points="all",
            x="subject",
            y="pieces",
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### How regularly do you report on surveillance by intelligence agencies? `[MSsoc4]`"
    )
    MSsoc4_counts = df[filter]["MSsoc4"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSsoc4_counts,
            values=MSsoc4_counts,
            names=MSsoc4_counts.index,
            color=MSsoc4_counts.index,
            color_discrete_map={
                "Very regularly": px.colors.qualitative.Prism[9],
                "Regularly": px.colors.qualitative.Prism[8],
                "Somewhat regularly": px.colors.qualitative.Prism[7],
                "Sometimes": px.colors.qualitative.Prism[6],
                "Rarely or never": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### When covering surveillance by intelligence agencies, which topics usually prompt you to write an article? `[MSsoc5]`"
    )
    MSsoc5_df = pd.DataFrame(columns=("option", "count", "country"))
    for label in [
        "follow_up_on_other_media",
        "statements_government",
        "oversight_reports",
        "leaks",
        "own_investigations",
        "dont_know",
        "prefer_not_to_say",
        "other",
    ]:
        MSsoc5_data = df[filter]["country"][df[f"MSsoc5[{label}]"] == 1].tolist()
        for i in MSsoc5_data:
            MSsoc5_df = MSsoc5_df.append(
                {"option": label, "count": MSsoc5_data.count(i), "country": i},
                ignore_index=True,
            )
    MSsoc5_df = MSsoc5_df.drop_duplicates()
    st.plotly_chart(
        render_histogram(
            MSsoc5_df,
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
        ),
        use_container_width=True,
    )

    st.write("### If you selected ???other???, please specify `[MSsoc5other]`")
    for i in df[filter]["MSsoc5other"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write(
        "### When covering surveillance by intelligence agencies, which of the following topics to you report on frequently? `[MSsoc6]`"
    )
    MSsoc6_df = pd.DataFrame(columns=("option", "count", "country"))
    for label in [
        "national_security_risks",
        "intelligence_success",
        "intelligence_misconduct",
        "oversight_interventions",
        "oversight_failures",
        "policy_debates_leg_reforms",
        "other",
    ]:
        MSsoc6_data = df[filter]["country"][df[f"MSsoc6[{label}]"] == 1].tolist()
        for i in MSsoc6_data:
            MSsoc6_df = MSsoc6_df.append(
                {"option": label, "count": MSsoc6_data.count(i), "country": i},
                ignore_index=True,
            )
    MSsoc6_df = MSsoc6_df.drop_duplicates()
    st.plotly_chart(
        render_histogram(
            MSsoc6_df,
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
        ),
        use_container_width=True,
    )

    st.write("### If you selected ???other???, please specify `[MSsoc6other]`")
    for i in df[filter]["MSsoc6other"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write("## Transnational Scope")

    st.write(
        "### How often does your work on surveillance by intelligence agencies cover a transnational angle? `[MStrans1]`"
    )
    MStrans1_counts = df[filter]["MStrans1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MStrans1_counts,
            values=MStrans1_counts,
            names=MStrans1_counts.index,
            color=MStrans1_counts.index,
            color_discrete_map={
                "Always": px.colors.qualitative.Prism[9],
                "Often (75% of the time)": px.colors.qualitative.Prism[8],
                "Sometimes (50% of the time)": px.colors.qualitative.Prism[7],
                "Rarely (25% of the time)": px.colors.qualitative.Prism[6],
                "Never": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### How often do you collaborate with colleagues covering other countries when working on surveillance by intelligence agencies? `[MStrans2]`"
    )
    MStrans2_counts = df[filter]["MStrans2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MStrans2_counts,
            values=MStrans2_counts,
            names=MStrans2_counts.index,
            color=MStrans2_counts.index,
            color_discrete_map={
                "Always": px.colors.qualitative.Prism[9],
                "Often (75% of the time)": px.colors.qualitative.Prism[8],
                "Sometimes (50% of the time)": px.colors.qualitative.Prism[7],
                "Rarely (25% of the time)": px.colors.qualitative.Prism[6],
                "Never": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Have those collaborations included an investigative research project with colleagues from abroad? `[MStrans3]`"
    )
    MStrans3_counts = df[filter]["MStrans3"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MStrans3_counts,
            values=MStrans3_counts,
            names=MStrans3_counts.index,
            color=MStrans3_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("## Perceived Impact")

    st.write(
        "### When you think about public responses to your articles on intelligence agencies by readers and colleagues, did you receive any of the following forms of public feedback or engagement? `[MSimpact1]`"
    )
    MSimpact1_df = pd.DataFrame(columns=("option", "count", "country"))
    for label in [
        "above_avg_comments",
        "above_avg_shares",
        "above_avg_readers",
        "letters_to_the_editor",
        "follow_up_by_other_media",
        "other",
        "none_of_the_above",
        "dont_know",
        "prefer_not_to_say",
    ]:
        MSimpact1_data = df[filter]["country"][df[f"MSimpact1[{label}]"] == 1].tolist()
        for i in MSimpact1_data:
            MSimpact1_df = MSimpact1_df.append(
                {"option": label, "count": MSimpact1_data.count(i), "country": i},
                ignore_index=True,
            )
    MSimpact1_df = MSimpact1_df.drop_duplicates()
    st.plotly_chart(
        render_histogram(
            MSsoc6_df,
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
        ),
        use_container_width=True,
    )

    st.write(
        "### When you think of responses to your articles on intelligence agencies by administrations or policy makers, did your reporting contribute to any of the following forms of political action? `[MSimpact2]`"
    )

    MSimpact2_df = pd.DataFrame(columns=("option", "count", "country"))
    for label in [
        "diplomatic_pressure",
        "civic_action",
        "conversations_with_government",
        "official_inquiries",
        "government_statements",
        "conversations_with_intelligence",
        "dont_know",
        "prefer_not_to_say",
        "other",
    ]:
        MSimpact2_data = df[filter]["country"][df[f"MSimpact2[{label}]"] == 1].tolist()
        for i in MSimpact2_data:
            MSimpact2_df = MSimpact2_df.append(
                {"option": label, "count": MSimpact2_data.count(i), "country": i},
                ignore_index=True,
            )
    MSimpact2_df = MSimpact2_df.drop_duplicates()
    st.plotly_chart(
        render_histogram(
            MSsoc6_df,
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
        ),
        use_container_width=True,
    )

    st.write("### If you selected ???other???, please specify `[MSimpact2other]`")
    for i in df[filter]["MSimpact2other"].to_list():
        if type(i) != float:
            st.write("- " + i)

if selected_section == "Protection":
    st.write("# Protection")

    st.write("## Operational Protection")

    st.write(
        "### Have you taken any of the following measures to protect your datas from attacks and surveillance? `[MSprotectops1]`"
    )
    MSprotectops1_options = [
        "Participation in digital security training",
        "Provision of secure drop or similar anonymous leaking platform",
        "Use of E2E encrypted communication channels",
    ]

    MSprotectops1_yes = []
    MSprotectops1_no = []
    MSprotectops1_dont_know = []
    MSprotectops1_prefer_not_to_say = []
    for answer in [
        "Yes",
        "No",
        "I don't know",
        "I prefer not to say",
    ]:
        for label in ["sectraining", "secure_drop", "e2e"]:
            try:
                count = df[filter][f"MSprotectops1[{label}]"].value_counts()[answer]
            except KeyError:
                count = 0
            if answer == "Yes":
                MSprotectops1_yes.append(count)
            elif answer == "No":
                MSprotectops1_no.append(count)
            elif answer == "I don't know":
                MSprotectops1_dont_know.append(count)
            elif answer == "I prefer not to say":
                MSprotectops1_prefer_not_to_say.append(count)
            else:
                continue

    st.plotly_chart(
        generate_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=MSprotectops1_options,
                    y=MSprotectops1_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=MSprotectops1_options,
                    y=MSprotectops1_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=MSprotectops1_options,
                    y=MSprotectops1_dont_know,
                    marker_color=px.colors.qualitative.Prism[10],
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=MSprotectops1_options,
                    y=MSprotectops1_prefer_not_to_say,
                    marker_color=px.colors.qualitative.Prism[10],
                ),
            ],
        )
    )

    st.write(
        "### Were any of these measures provided by your employer? `[MSprotectops2]`"
    )
    MSprotectops2_counts = df[filter]["MSprotectops2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=MSprotectops2_counts,
            names=MSprotectops2_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
        ),
        use_container_width=True,
    )

    st.write(
        "### How important is the use of the following technical tools for you to protect your communications, your online activities and the data you handle? `[MSprotectops3]`"
    )
    MSprotectops3_options = [
        "Encrypted Email",
        "VPN",
        "Tor",
        "E2E Messengers",
        "Encrpyted hardware",
        "Two-Factor authentication",
        "Other",
    ]

    MSprotectops3_very_important = []
    MSprotectops3_somewhat_important = []
    MSprotectops3_important = []
    MSprotectops3_slightly_important = []
    MSprotectops3_not_important = []
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
                count = df[filter][f"MSprotectops3[{label}]"].value_counts()[importance]
            except KeyError:
                count = 0
            if importance == "Very important":
                MSprotectops3_very_important.append(count)
            elif importance == "Somewhat important":
                MSprotectops3_somewhat_important.append(count)
            elif importance == "Important":
                MSprotectops3_important.append(count)
            elif importance == "Slightly important":
                MSprotectops3_slightly_important.append(count)
            elif importance == "Not important at all":
                MSprotectops3_not_important.append(count)
            else:
                continue

    st.plotly_chart(
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Very important",
                    x=MSprotectops3_options,
                    y=MSprotectops3_very_important,
                    marker_color="#581845",
                ),
                go.Bar(
                    name="Somewhat important",
                    x=MSprotectops3_options,
                    y=MSprotectops3_somewhat_important,
                    marker_color="#900C3F",
                ),
                go.Bar(
                    name="Important",
                    x=MSprotectops3_options,
                    y=MSprotectops3_important,
                    marker_color="#C70039",
                ),
                go.Bar(
                    name="Slightly important",
                    x=MSprotectops3_options,
                    y=MSprotectops3_slightly_important,
                    marker_color="#FF5733",
                ),
                go.Bar(
                    name="Not important at all",
                    x=MSprotectops3_options,
                    y=MSprotectops3_not_important,
                    marker_color="#FFC300",
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write("### If you selected ???other???, please specify `[MSprotectops3other]`")
    for i in df[filter]["MSprotectops3other"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write(
        "### Which of the following statements best describes your level of confidence in the protection offered by technological tools? `[MSprotectops4]`"
    )
    MSprotectops4_counts = df[filter]["MSprotectops4"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSprotectops4_counts,
            values=MSprotectops4_counts,
            names=MSprotectops4_counts.index,
            color=MSprotectops4_counts.index,
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
        ),
        use_container_width=True,
    )

    st.write("## Legal Protection")

    # TODO Clarify that in MS it's about source protection (also for MSprotectleg2)
    st.write(
        "### When working on intelligence-related issues, do you feel you have reason to be concerned about surveillance of your activities `[MSprotectleg1]`"
    )

    MSprotectleg1_counts = df[filter]["MSprotectleg1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=MSprotectleg1_counts,
            names=MSprotectleg1_counts.index,
            color=MSprotectleg1_counts.index,
            color_discrete_map={
                "Always": px.colors.qualitative.Prism[9],
                "Often": px.colors.qualitative.Prism[8],
                "Sometimes": px.colors.qualitative.Prism[7],
                "Rarely": px.colors.qualitative.Prism[6],
                "Never": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Do you regard the existing legal protections against surveillance of your activities in your country as a sufficient safeguard for your work on intelligence-related issues? `[MSprotectleg2]`"
    )

    MSprotectleg2_counts = df[filter]["MSprotectleg2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSprotectleg2_counts,
            values=MSprotectleg2_counts,
            names=MSprotectleg2_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
            color=MSprotectleg2_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Are any of the following forms of institutional support readily available to you? `[MSprotectleg3]`"
    )
    MSprotectleg3_options = ["Free legal counsel", "Legal cost insurance", "Other"]
    MSprotectleg3_yes = []
    MSprotectleg3_no = []
    MSprotectleg3_dont_know = []
    MSprotectleg3_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in ["free_counsel", "cost_insurance", "other"]:
            try:
                count = df[filter][f"MSprotectleg3[{label}]"].value_counts()[answer]
            except KeyError:
                count = 0
            if answer == "Yes":
                MSprotectleg3_yes.append(count)
            elif answer == "No":
                MSprotectleg3_no.append(count)
            elif answer == "I don't know":
                MSprotectleg3_dont_know.append(count)
            elif answer == "I prefer not to say":
                MSprotectleg3_prefer_not_to_say.append(count)
            else:
                continue
    st.plotly_chart(
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=MSprotectleg3_options,
                    y=MSprotectleg3_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=MSprotectleg3_options,
                    y=MSprotectleg3_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=MSprotectleg3_options,
                    y=MSprotectleg3_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=MSprotectleg3_options,
                    y=MSprotectleg3_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write("### If you selected ???other???, please specify `[MSprotectleg3other]`")
    for i in df[filter]["MSprotectleg3other"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write(
        "### Over the past 5 years, have you made use of any of the below-mentioned forms of institutional support? `[MSprotectleg4]`"
    )
    MSprotectleg4_options = ["Free legal counsel", "Legal cost insurance", "Other"]
    MSprotectleg4_yes = []
    MSprotectleg4_no = []
    MSprotectleg4_dont_know = []
    MSprotectleg4_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in ["free_counsel", "cost_insurance", "other"]:
            try:
                count = df[filter][f"MSprotectleg4[{label}]"].value_counts()[answer]
            except KeyError:
                count = 0
            if answer == "Yes":
                MSprotectleg4_yes.append(count)
            elif answer == "No":
                MSprotectleg4_no.append(count)
            elif answer == "I don't know":
                MSprotectleg4_dont_know.append(count)
            elif answer == "I prefer not to say":
                MSprotectleg4_prefer_not_to_say.append(count)
            else:
                continue
    st.plotly_chart(
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=MSprotectleg4_options,
                    y=MSprotectleg4_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=MSprotectleg4_options,
                    y=MSprotectleg4_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=MSprotectleg4_options,
                    y=MSprotectleg4_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=MSprotectleg4_options,
                    y=MSprotectleg4_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write("### If you selected ???other???, please specify `[MSprotectleg4other]`")
    for i in df[filter]["MSprotectleg4other"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write(
        "### In your experience, how common is it for news organisations to assume liabilities for the content of published articles? `[MSprotectleg5]`"
    )
    MSprotectleg5_counts = df[filter]["MSprotectleg5"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSprotectleg5_counts,
            values=MSprotectleg5_counts,
            names=MSprotectleg5_counts.index,
            color=MSprotectleg5_counts.index,
            color_discrete_map={
                "Very common": px.colors.qualitative.Prism[9],
                "Common": px.colors.qualitative.Prism[8],
                "Somewhat common": px.colors.qualitative.Prism[7],
                "Slightly common": px.colors.qualitative.Prism[6],
                "Not common at all": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("## Rights to Access")

    st.write(
        "### As a journalist in the country you primarily work in, do you have a special right to know if you have been subjected to surveillance in the past? `[MSprotectrta1]`"
    )
    MSprotectrta1_counts = df[filter]["MSprotectrta1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSprotectrta1_counts,
            values=MSprotectrta1_counts,
            names=MSprotectrta1_counts.index,
            color=MSprotectrta1_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("### Have you ever made use of this right? `[MSprotectrta2]`")
    MSprotectrta2_counts = df[filter]["MSprotectrta2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSprotectrta2_counts,
            values=MSprotectrta2_counts,
            names=MSprotectrta2_counts.index,
            color=MSprotectrta2_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Is this right available to all journalists, even non-citizens? `[MSprotectrta3]`"
    )
    MSprotectrta3_counts = df[filter]["MSprotectrta3"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSprotectrta3_counts,
            values=MSprotectrta3_counts,
            names=MSprotectrta3_counts.index,
            color=MSprotectrta3_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Have you ever submitted a data subject access request (based on your right to access as defined in the GDPR) related to surveillance by intelligence agencies? `[MSprotectrta4]`"
    )
    MSprotectrta4_counts = df[filter]["MSprotectrta4"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSprotectrta4_counts,
            values=MSprotectrta4_counts,
            names=MSprotectrta4_counts.index,
            color=MSprotectrta4_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Over the past 5 years, have you received responses to your data subject access request(s) in a timely manner? `[MSprotectrta5]`"
    )
    MSprotectrta5_counts = df[filter]["MSprotectrta5"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSprotectrta5_counts,
            values=MSprotectrta5_counts,
            names=MSprotectrta5_counts.index,
            color=MSprotectrta5_counts.index,
            color_discrete_map={
                "Never": px.colors.qualitative.Prism[9],
                "No, usually longer than 30 days": px.colors.qualitative.Prism[8],
                "Yes, within 30 days": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### If you received a response to a data subject access request, was the information provided helpful? `[MSprotectrta6]`"
    )
    MSprotectrta6_counts = df[filter]["MSprotectrta6"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSprotectrta6_counts,
            values=MSprotectrta6_counts,
            names=MSprotectrta6_counts.index,
            color=MSprotectrta6_counts.index,
            color_discrete_map={
                "Yes, the information provided was helpful": px.colors.qualitative.Prism[
                    2
                ],
                "Partly, the information provided was somewhat <br>helpful but contained omissions": px.colors.qualitative.Prism[
                    8
                ],
                "No, the information provided was not at all helpful": px.colors.qualitative.Prism[
                    9
                ],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

if selected_section == "Constraints":
    st.write("# Constraints")

    st.write("## Censorship")

    st.write(
        "### When covering intelligence related issues, have you consulted state bodies or officials prior to the publication of the story due to the sensitivity of information? `[MSconstraintcen1]`"
    )
    MSconstraintcen1_counts = df[filter]["MSconstraintcen1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSconstraintcen1_counts,
            values=MSconstraintcen1_counts,
            names=MSconstraintcen1_counts.index,
            color=MSconstraintcen1_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Is there an institutional setting that advises journalists to engage in a consultation process prior to the publication of sensitive information (i.e. a code of conduct or a committee)? `[MSconstraintcen2]`"
    )
    MSconstraintcen2_counts = df[filter]["MSconstraintcen2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSconstraintcen2_counts,
            values=MSconstraintcen2_counts,
            names=MSconstraintcen2_counts.index,
            color=MSconstraintcen2_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Please estimate: How often have you consulted state bodies or officials prior to publishing  intelligence-related stories in the past 5 years? `[MSconstraintcen3]`"
    )
    st.plotly_chart(
        render_histogram(
            df=df[filter],
            x="MSconstraintcen3",
            y=None,
            nbins=10,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"MSconstraintcen3": "times"},
        ),
        use_container_width=True,
    )

    st.write(
        "### Has this consultation process prevented a publication of yours from appearing? `[MSconstraintcen4]`"
    )
    MSconstraintcen4_counts = df[filter]["MSconstraintcen4"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSconstraintcen4_counts,
            values=MSconstraintcen4_counts,
            names=MSconstraintcen4_counts.index,
            color=MSconstraintcen4_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("### If you selected ???yes???, please specify `[MSconstraintcen4spec]`")
    for i in df[filter]["MSconstraintcen4spec"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write(
        "### Have you been required to make edits as part of this consultation process? `[MSconstraintcen5]`"
    )
    MSconstraintcen5_counts = df[filter]["MSconstraintcen5"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            MSconstraintcen5_counts,
            values=MSconstraintcen5_counts,
            names=MSconstraintcen5_counts.index,
            color=MSconstraintcen5_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("### If you selected ???yes???, please specify `[MSconstraintcen5spec]`")
    for i in df[filter]["MSconstraintcen5spec"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write("## Interference")

    st.write(
        "### Has your institution or have you yourself been subjected to surveillance by intelligence agencies in the past five years? `[MSconstraintinter1]`"
    )

    MSconstraintinter1_counts = df[filter]["MSconstraintinter1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=MSconstraintinter1_counts,
            names=MSconstraintinter1_counts.index,
            color=MSconstraintinter1_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes, I have evidence": px.colors.qualitative.Prism[1],
                "Yes, I suspect": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### In the past 5 years, have you been threatened with prosecution or have you actually been prosecuted for your work on intelligence-related issues? `[MSconstraintinter2]`"
    )

    MSconstraintinter2_counts = df[filter]["MSconstraintinter2"].value_counts()
    MSconstraintinter2_fig = px.pie(
        df[filter],
        values=MSconstraintinter2_counts,
        names=MSconstraintinter2_counts.index,
        color_discrete_sequence=px.colors.qualitative.Prism,
    )

    st.plotly_chart(MSconstraintinter2_fig)

    st.write("### What was the outcome? `[MSconstraintinter3]`")

    MSconstraintinter3_counts = df[filter]["MSconstraintinter3"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=MSconstraintinter3_counts,
            names=MSconstraintinter3_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
        ),
        use_container_width=True,
    )

    st.write(
        "### In the past 5 years, have you experienced any of the following interferences by public authorities in relation to your work on intelligence related topics? `[MSconstraintinter4]`"
    )
    # TODO Map proper labels
    MSconstraintinter4_yes = []
    MSconstraintinter4_no = []
    MSconstraintinter4_dont_know = []
    MSconstraintinter4_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in MSconstraintinter4_options:
            try:
                count = df[filter][f"MSconstraintinter4[{label}]"].value_counts()[
                    answer
                ]
            except KeyError:
                count = 0
            if answer == "Yes":
                MSconstraintinter4_yes.append(count)
            elif answer == "No":
                MSconstraintinter4_no.append(count)
            elif answer == "I don't know":
                MSconstraintinter4_dont_know.append(count)
            elif answer == "I prefer not to say":
                MSconstraintinter4_prefer_not_to_say.append(count)
            else:
                continue
    st.plotly_chart(
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=MSconstraintinter4_options,
                    y=MSconstraintinter4_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=MSconstraintinter4_options,
                    y=MSconstraintinter4_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=MSconstraintinter4_options,
                    y=MSconstraintinter4_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=MSconstraintinter4_options,
                    y=MSconstraintinter4_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write(
        "### In the past 5 years, have you been approached by intelligence officials and received... `[MSconstraintinter5]`"
    )
    MSconstraintinter5_options = [
        "Unsolicited information",
        "Invitations to off-the-record events or meetings",
        "Other",
    ]
    MSconstraintinter5_yes = []
    MSconstraintinter5_no = []
    MSconstraintinter5_dont_know = []
    MSconstraintinter5_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in ["unsolicited_information", "invitations", "other"]:
            try:
                count = df[filter][f"MSconstraintinter5[{label}]"].value_counts()[
                    answer
                ]
            except KeyError:
                count = 0
            if answer == "Yes":
                MSconstraintinter5_yes.append(count)
            elif answer == "No":
                MSconstraintinter5_no.append(count)
            elif answer == "I don't know":
                MSconstraintinter5_dont_know.append(count)
            elif answer == "I prefer not to say":
                MSconstraintinter5_prefer_not_to_say.append(count)
            else:
                continue
    st.plotly_chart(
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=MSconstraintinter5_options,
                    y=MSconstraintinter5_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=MSconstraintinter5_options,
                    y=MSconstraintinter5_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=MSconstraintinter5_options,
                    y=MSconstraintinter5_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=MSconstraintinter5_options,
                    y=MSconstraintinter5_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write("### If you selected ???other???, please specify `[MSconstraintinter5other]`")
    for i in df[filter]["MSconstraintinter5other"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write(
        "### When working on intelligence-related issues have you ever experienced harassment by security agencies or politicians due to your... `[MSconstraintinter6]`"
    )
    MSconstraintinter6_options = [
        "Gender",
        "Ethnicity",
        "Political orientation",
        "Sexual orientation",
        "Religious affiliation",
        "Other",
    ]
    MSconstraintinter6_yes = []
    MSconstraintinter6_no = []
    MSconstraintinter6_dont_know = []
    MSconstraintinter6_prefer_not_to_say = []
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
                count = df[filter][f"MSconstraintinter6[{label}]"].value_counts()[
                    answer
                ]
            except KeyError:
                count = 0
            if answer == "Yes":
                MSconstraintinter6_yes.append(count)
            elif answer == "No":
                MSconstraintinter6_no.append(count)
            elif answer == "I don't know":
                MSconstraintinter6_dont_know.append(count)
            elif answer == "I prefer not to say":
                MSconstraintinter6_prefer_not_to_say.append(count)
            else:
                continue
    st.plotly_chart(
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=MSconstraintinter6_options,
                    y=MSconstraintinter6_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=MSconstraintinter6_options,
                    y=MSconstraintinter6_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=MSconstraintinter6_options,
                    y=MSconstraintinter6_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=MSconstraintinter6_options,
                    y=MSconstraintinter6_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write("### If you selected ???other???, please specify `[MSconstraintinter6other]`")
    for i in df[filter]["MSconstraintinter6other"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write("## Self-Censorship")

    st.write(
        "### Which of the following behaviours have you experienced or observed in your professional environment related to covering intelligence-related topics? `[MSconstraintself1]`"
    )
    MSconstraintself1_options = [
        "Avoided sensitive issues in a story related to intelligence",
        "Changed the focus of a story related to intelligence",
        "Changed the timeline for publication",
        "Abandoned a story related to intelligence",
        "Considered leaving the profession altogether",
        "Other",
    ]
    MSconstraintself1_yes = []
    MSconstraintself1_no = []
    MSconstraintself1_dont_know = []
    MSconstraintself1_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in [
            "avoid",
            "change_focus",
            "change_timeline",
            "abandon",
            "leave_profession",
            "other",
        ]:
            try:
                count = df[filter][f"MSconstraintself1[{label}]"].value_counts()[answer]
            except KeyError:
                count = 0
            if answer == "Yes":
                MSconstraintself1_yes.append(count)
            elif answer == "No":
                MSconstraintself1_no.append(count)
            elif answer == "I don't know":
                MSconstraintself1_dont_know.append(count)
            elif answer == "I prefer not to say":
                MSconstraintself1_prefer_not_to_say.append(count)
            else:
                continue
    st.plotly_chart(
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=MSconstraintself1_options,
                    y=MSconstraintself1_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=MSconstraintself1_options,
                    y=MSconstraintself1_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=MSconstraintself1_options,
                    y=MSconstraintself1_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=MSconstraintself1_options,
                    y=MSconstraintself1_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write("### If you selected ???other???, please specify `[MSconstraintself1other]`")
    for i in df[filter]["MSconstraintself1other"].to_list():
        if type(i) != float:
            st.write("- " + i)

if selected_section == "Attitudes":
    st.write("# Attitudes")

    st.write(
        "### The following four statements are about **intelligence agencies**. Please select the statement you most agree with, based on your national context. `[MSattitude1]`"
    )

    MSattitude1_counts = df[filter]["MSattitude1"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=MSattitude1_counts,
            names=MSattitude1_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
        ),
        use_container_width=True,
    )

    # Pie chart MSattitudes (MSattitude2)
    st.write(
        "### The following four statements are about **intelligence oversight**. Please select the statement you most agree with, based on your national context. `[MSattitude2]`"
    )

    MSattitude2_counts = df[filter]["MSattitude2"].value_counts()
    st.plotly_chart(
        render_pie_chart(
            df[filter],
            values=MSattitude2_counts,
            names=MSattitude2_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
        ),
        use_container_width=True,
    )

    # Histogram (MSattitude3)
    # TODO Map proper labels
    st.write(
        "### In your personal view, what are the goals of intelligence oversight? Please select the three goals of oversight you subscribe to the most.??`[MSattitude3]`"
    )
    MSattitude3_options = [
        "rule_of_law",
        "civil_liberties",
        "effectiveness_of_intel",
        "legitimacy_of_intel",
        "trust_in_intel",
        "critique_of_intel",
        "prefer_not_to_say",
    ]
    MSattitude3_df = pd.DataFrame(columns=("option", "count", "country"))
    for label in MSattitude3_options:
        MSattitude3_data = df[filter]["country"][
            df[f"MSattitude3[{label}]"] == 1
        ].tolist()
        for i in MSattitude3_data:
            MSattitude3_df = MSattitude3_df.append(
                {"option": label, "count": MSattitude3_data.count(i), "country": i},
                ignore_index=True,
            )
    MSattitude3_df = MSattitude3_df.drop_duplicates()
    st.plotly_chart(
        render_histogram(
            df=MSattitude3_df,
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
        ),
        use_container_width=True,
    )

    scoring = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}
    bodies = [
        "Parliamentary oversight bodies",
        "Judicial oversight bodies",
        "Independent expert bodies",
        "Data protection authorities",
        "Audit courts",
        "Civil society organisations",
    ]

    st.write(
        "### Which of the following actors do you trust the most to **enable public debate** on surveillance by intelligence agencies???`[MSattitude4]`"
    )
    st.plotly_chart(render_ranking_plot("MSattitude4"), use_container_width=True)

    st.write(
        "### Which of the following actors do you trust the most to **contest surveillance** by intelligence agencies???`[MSattitude5]`"
    )
    st.plotly_chart(render_ranking_plot("MSattitude5"), use_container_width=True)

    st.write(
        "### Which of the following actors do you trust the most to **enforce compliance** regarding surveillance by intelligence agencies???`[MSattitude6]`"
    )
    st.plotly_chart(render_ranking_plot("MSattitude6"), use_container_width=True)


if selected_section == "Appendix":
    st.write("# Appendix")

    st.write("## Raw data")

    st.write(get_csv_download_link(df, "media"), unsafe_allow_html=True)
    st.write(get_excel_download_link(df, "media"), unsafe_allow_html=True)

    table = st.checkbox("Show data as table")
    if table:
        st.dataframe(df[filter])

    st.write("## Correlation Matrix (Phik `??K`)")

    st.write(
        "Phik (??k) is a new and practical correlation coefficient that works consistently between categorical, ordinal and interval variables, captures non-linear dependency and reverts to the Pearson correlation coefficient in case of a bivariate normal input distribution. There is extensive documentation available [here](https://phik.readthedocs.io/en/latest/index.html)"
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

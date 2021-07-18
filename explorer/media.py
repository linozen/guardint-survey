import streamlit as st
import pandas as pd
import numpy as np
import phik
import plotly.express as px
import base64
from io import BytesIO

# Factors to filter by (MS only)
# ------------------------------
# MShr1
# MSgender
# MSattitude1-2

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
# General configuration
###################################################################################
st.set_page_config(
    page_title="IOI Survey Data Explorer (MS only)",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("IOI Survey Data Explorer (MS only)")

###################################################################################
# Data acquisition
###################################################################################


@st.cache(allow_output_mutation=True)
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
            "MSconstraintcen5",
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


###################################################################################
# Define DataFrame
###################################################################################
df = get_ms_df()
df = df.reset_index(drop=True)

###################################################################################
# Make answers human-readable
###################################################################################
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
        "AO05": "I prefere not to say",
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
        "AO002": "Often",
        "AO003": "Sometimes",
        "AO004": "Rarely",
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
            "AO01": "Very important",
            "AO02": "Important",
            "AO03": "Somewhat important",
            "AO04": "Slightly important",
            "AO05": "Not important at all",
            "AO06": "I don't know",
            "AO07": "I prefer not to say",
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
        "AO01": "Yes, my request(s) were responded to in a timely manner of up to 30 days",
        "AO02": "No my request(s) were not responded to in a timely manner and often took longer than 30 days",
        "AO03": "I never received responses to my request(s)",
        "AO04": "I don't know",
        "AO05": "I prefer not to say",
    }
)

df["MSprotectrta6"] = df["MSprotectrta6"].replace(
    {
        "AO01": "Yes, the information provided was helpful",
        "AO02": "Partly, the information provided was somewhat helpful but contained omissions",
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

df["MSgender"] = df["MSgender"].replace(
    {
        "AO01": "Woman",
        "AO02": "Non-binary",
        "AO03": "Man",
        "AO04": "I prefer not to say",
        "AO05": "Other",
    }
)
###################################################################################
# Make answers analysable (change data types etc.)
###################################################################################
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
        or col.startswith("MSsoc5")
        or col.startswith("MSsoc6")
        or col.startswith("MSimpact1")
        or col.startswith("MSimpact2")
        or col.startswith("MSattitude3")
    ):
        df[col] = df[col].replace(np.nan, False)
        df[col] = df[col].replace("Y", True)
        df[col] = df[col].astype("bool")
###################################################################################
# Filter logic
###################################################################################
# TODO filter by attitudes1-2
filters = {
    "country": st.sidebar.selectbox(
        "Country", ["All", "United Kingdom", "Germany", "France"]
    ),
    "MShr1": st.sidebar.selectbox(
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
}

filter = np.full(len(df.index), True)
for column_name, selectbox in filters.items():
    if selectbox == "All":
        continue
    else:
        filter = filter & (df[column_name] == selectbox)

###################################################################################
# Provide download links
###################################################################################
# Save a useful snapshot of the merged data
df.to_pickle("./data/media.pkl")
df.to_excel("./data/media.xlsx")
df.to_csv("./data/media.csv")


@st.cache
def get_csv_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="ioi_media_only.csv">Download as CSV file</a>'
    return href


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1")
    writer.save()
    processed_data = output.getvalue()
    return processed_data


@st.cache
def get_excel_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="ioi_media_only.xlsx">Download as Excel file</a>'


st.write(get_csv_download_link(df), unsafe_allow_html=True)
st.write(get_excel_download_link(df), unsafe_allow_html=True)

###################################################################################
# Display table
###################################################################################
st.dataframe(df[filter], height=1000)

###################################################################################
# Display dynamic charts
###################################################################################
# Correlation matrix


@st.cache
def generate_corr_matrix(df):
    df = df.phik_matrix()
    fig = px.imshow(df, zmin=0, zmax=1, color_continuous_scale="viridis", height=1300)
    return fig


@st.cache
def generate_significance_matrix(df):
    df = df.significance_matrix(significance_method="asymptotic")
    fig = px.imshow(df, zmin=-5, zmax=5, color_continuous_scale="viridis", height=1300)
    return fig


st.write(
    "# Correlation Matrix (Phik `φK`) \nPhik (φk) is a new and practical correlation coefficient that works consistently between categorical, ordinal and interval variables, captures non-linear dependency and reverts to the Pearson correlation coefficient in case of a bivariate normal input distribution. There is extensive documentation available [here](https://phik.readthedocs.io/en/latest/index.html)"
)

fig_corr = generate_corr_matrix(df)
st.plotly_chart(fig_corr, use_container_width=True)

st.write("# Significance Matrix")
st.markdown(
    body="When assessing correlations it is good practise to evaluate both the correlation and the significance of the correlation: a large correlation may be statistically insignificant, and vice versa a small correlation may be very significant. For instance, scipy.stats.pearsonr returns both the pearson correlation and the p-value. Similarly, the phik package offers functionality the calculate a significance matrix. Significance is defined as: "
)
st.markdown(
    body="$Z=\Phi^{-1}(1-p); \Phi(z)=\\frac{1}{\\sqrt{2\pi}}\int_{-\infty}^{z} e^{-t^{2}/2}\,dt$"
)

fig_sig = generate_significance_matrix(df)
st.plotly_chart(fig_sig, use_container_width=True)

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

###################################################################################
# General configuration
###################################################################################
st.set_page_config(
    page_title="IOI Survey Data Explorer (CS only)",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("IOI Survey Data Explorer (CS only)")

###################################################################################
# Data acquisition
###################################################################################


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
            # =======
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
# Define DataFrame
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
            "AO01": "Very important",
            "AO02": "Important",
            "AO03": "Somewhat important",
            "AO04": "Slightly important",
            "AO05": "Not important at all",
            "AO06": "I don't know",
            "AO07": "I prefer not to say",
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

    df[f"CSprotectops3[{label}]"] = df[f"CSprotectops3[{label}]"].replace(
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
                "AO06": "Civil society organisations",
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
                "AO06": "Civil society organisations",
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
###################################################################################
# Make answers analysable (change data types etc.)
###################################################################################
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
        or col.startswith("CSfoi5")
        or col.startswith("CSsoc5")
        or col.startswith("CSsoc6")
        or col.startswith("CSimpact1")
        or col.startswith("CSimpact2")
        or col.startswith("CSattitude3")
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
    "CShr1": st.sidebar.selectbox(
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
df.to_pickle("./data/civsoc.pkl")
df.to_excel("./data/civsoc.xlsx")
df.to_csv("./data/civsoc.csv")


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
    href = f'<a href="data:file/csv;base64,{b64}" download="ioi_civsoc_only.csv">Download as CSV file</a>'
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
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="ioi_civsoc_only.xlsx">Download as Excel file</a>'


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
def get_corr_matrix(df):
    df = pd.read_pickle("./data/civsoc_corr.pkl")
    fig = px.imshow(df, zmin=0, zmax=1, color_continuous_scale="viridis", height=1300)
    return fig


@st.cache
def get_significance_matrix(df):
    df = pd.read_pickle("./data/civsoc_sig.pkl")
    fig = px.imshow(df, zmin=-5, zmax=5, color_continuous_scale="viridis", height=1300)
    return fig


st.write(
    "# Correlation Matrix (Phik `φK`) \nPhik (φk) is a new and practical correlation coefficient that works consistently between categorical, ordinal and interval variables, captures non-linear dependency and reverts to the Pearson correlation coefficient in case of a bivariate normal input distribution. There is extensive documentation available [here](https://phik.readthedocs.io/en/latest/index.html)"
)

df_without_act = df[
    df.columns.drop(list(df.filter(regex="campact.*|advocact.*|litigateact.*")))
]


fig_corr = get_corr_matrix(df_without_act)
st.plotly_chart(fig_corr, use_container_width=True)

st.write("# Significance Matrix")
st.markdown(
    body="When assessing correlations it is good practise to evaluate both the correlation and the significance of the correlation: a large correlation may be statistically insignificant, and vice versa a small correlation may be very significant. For instance, scipy.stats.pearsonr returns both the pearson correlation and the p-value. Similarly, the phik package offers functionality the calculate a significance matrix. Significance is defined as: "
)
st.markdown(
    body="$Z=\Phi^{-1}(1-p); \Phi(z)=\\frac{1}{\\sqrt{2\pi}}\int_{-\infty}^{z} e^{-t^{2}/2}\,dt$"
)

fig_sig = get_significance_matrix(df_without_act)
st.plotly_chart(fig_sig, use_container_width=True)

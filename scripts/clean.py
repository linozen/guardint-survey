#!/usr/bin/env python3
import pandas as pd
import numpy as np


def construct_cs_df():

    # Merge CSV files into DataFrame
    cs_csv_files = [
        "data/limesurvey/cs_uk_short.csv",
        "data/limesurvey/cs_de_short.csv",
        "data/limesurvey/cs_fr_short.csv",
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
            "CSfinance2[SQ01]": "CSfinance2cs[private_foundations]",
            "CSfinance2[SQ02]": "CSfinance2cs[donations]",
            "CSfinance2[SQ03]": "CSfinance2cs[national_public_funds]",
            "CSfinance2[SQ04]": "CSfinance2cs[corporate_sponsorship]",
            "CSfinance2[SQ05]": "CSfinance2cs[international_public_funds]",
            "CSfinance2[SQ06]": "CSfinance2cs[other]",
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
            # "CSconstraintinter5ot": "CSconstraintinter5other",
            "CSconstraintinter6[SQ01]": "CSconstraintinter6[gender]",
            "CSconstraintinter6[SQ02]": "CSconstraintinter6[ethnicity]",
            "CSconstraintinter6[SQ03]": "CSconstraintinter6[political]",
            "CSconstraintinter6[SQ04]": "CSconstraintinter6[sexual]",
            "CSconstraintinter6[SQ05]": "CSconstraintinter6[religious]",
            "CSconstraintinter6[SQ06]": "CSconstraintinter6[other]",
            # "CSconstraintinter6ot": "CSconstraintinter6other",
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
            "CSfinance2cs[private_foundations]",
            "CSfinance2cs[donations]",
            "CSfinance2cs[national_public_funds]",
            "CSfinance2cs[corporate_sponsorship]",
            "CSfinance2cs[international_public_funds]",
            "CSfinance2cs[other]",
            # "CSfinance2other",
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
            # "CSfoi5other",
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
            # "CSprotectops3other",
            "CSprotectops4",
            "CSprotectleg1",
            "CSprotectleg2",
            # "CSprotectleg2no",
            "CSprotectleg3[free_counsel]",
            "CSprotectleg3[cost_insurance]",
            "CSprotectleg3[other]",
            # "CSprotectleg3other",
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
            # "CSconstraintinter5other",
            "CSconstraintinter6[gender]",
            "CSconstraintinter6[ethnicity]",
            "CSconstraintinter6[political]",
            "CSconstraintinter6[sexual]",
            "CSconstraintinter6[religious]",
            "CSconstraintinter6[other]",
            # "CSconstraintinter6other",
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

    # Set field
    df["field"] = "CSO Professionals"
    return df


def construct_ms_df():
    # Merge CSV files into DataFrame
    ms_csv_files = [
        "data/limesurvey/ms_uk_short.csv",
        "data/limesurvey/ms_de_short.csv",
        "data/limesurvey/ms_fr_short.csv",
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
            "MSfinance2": "MSfinance2ms",
            "MFfoi2": "MSfoi2",
            "MShr3[SQ01]": "MShr3ms[daily_newspaper]",
            "MShr3[SQ02]": "MShr3ms[weekly_newspaper]",
            "MShr3[SQ03]": "MShr3ms[magazine]",
            "MShr3[SQ04]": "MShr3ms[tv]",
            "MShr3[SQ05]": "MShr3ms[radio]",
            "MShr3[SQ06]": "MShr3ms[news_agency]",
            "MShr3[SQ07]": "MShr3ms[online_stand_alone]",
            "MShr3[SQ08]": "MShr3ms[online_of_offline]",
            "MShr4": "MShr4ms",
            "MSfoi5[SQ01]": "MSfoi5[not_aware]",
            "MSfoi5[SQ02]": "MSfoi5[not_covered]",
            "MSfoi5[SQ03]": "MSfoi5[too_expensive]",
            "MSfoi5[SQ04]": "MSfoi5[too_time_consuming]",
            "MSfoi5[SQ05]": "MSfoi5[afraid_of_data_destruction]",
            "MSfoi5[SQ06]": "MSfoi5[afraid_of_discrimination]",
            "MSfoi5[SQ07]": "MSfoi5[other]",
            "MSfoi5[SQ08]": "MSfoi5[dont_know]",
            "MSfoi5[SQ09]": "MSfoi5[prefer_not_to_say]",
            # "MSfoi5specify": "MSfoi5other",
            "MScontstraintinter1": "MSconstraintinter1",
            "MSprotectleg2A": "MSprotectleg2",
            # "MSprotectleg2Ano": "MSprotectleg2no",
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
            # "MSconstraintinter5ot": "MSconstraintinter5other",
            "MSconstraintinter6[SQ01]": "MSconstraintinter6[gender]",
            "MSconstraintinter6[SQ02]": "MSconstraintinter6[ethnicity]",
            "MSconstraintinter6[SQ03]": "MSconstraintinter6[political]",
            "MSconstraintinter6[SQ04]": "MSconstraintinter6[sexual]",
            "MSconstraintinter6[SQ05]": "MSconstraintinter6[religious]",
            "MSconstraintinter6[SQ06]": "MSconstraintinter6[other]",
            # "MSconstraintinter6ot": "MSconstraintinter6other",
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
            "MShr3ms[daily_newspaper]",
            "MShr3ms[weekly_newspaper]",
            "MShr3ms[magazine]",
            "MShr3ms[tv]",
            "MShr3ms[radio]",
            "MShr3ms[news_agency]",
            "MShr3ms[online_stand_alone]",
            "MShr3ms[online_of_offline]",
            "MShr4ms",
            "MSgender",
            "MSexpertise1",
            "MSexpertise2",
            "MSexpertise3",
            "MSexpertise4",
            "MSfinance1",
            "MSfinance2ms",
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
            "MSfoi5[dont_know]",
            "MSfoi5[prefer_not_to_say]",
            # "MSfoi5other",
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
            # "MSprotectops3other",
            "MSprotectops4",
            "MSprotectleg1",
            "MSprotectleg2",
            # "MSprotectleg2no",
            "MSprotectleg3[free_counsel]",
            "MSprotectleg3[cost_insurance]",
            "MSprotectleg3[other]",
            # "MSprotectleg3other",
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
            # "MSconstraintinter5other",
            "MSconstraintinter6[gender]",
            "MSconstraintinter6[ethnicity]",
            "MSconstraintinter6[political]",
            "MSconstraintinter6[sexual]",
            "MSconstraintinter6[religious]",
            "MSconstraintinter6[other]",
            # "MSconstraintinter6other",
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

    # Set field
    df["field"] = "Media Professionals"
    return df


# ===========================================================================
# Merge MS and CS DataFrames
# ===========================================================================
df_cs = construct_cs_df()
df_ms = construct_ms_df()
df = pd.concat([df_cs, df_ms], ignore_index=True)

# Helper variables needed when answers are coded differently in the
# respective survey types or languages
is_civsoc = df.field == "CSO Professionals"
is_media = df.field == "Media Professionals"
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

df["hr4ms"] = df["hr4ms"].replace(
    {
        "AO01": "A1: I had enough time",
        "AO02": "A2: I had some time",
        "AO03": "A3: I had very little time",
        "AO04": "A4: I had no time",
        "AO05": "A5: I don't know",
        "AO06": "A6: I prefer not to say",
    }
)

df["gender"] = df["gender"].fillna("Not specified")
df["gender"] = df["gender"].replace(
    {
        "AO01": "Female",
        "AO02": "Non-binary",
        "AO03": "Male",
        "AO04": "I prefer not to say",
        "AO05": "Other",
    }
)

df["expertise2"] = df["expertise2"].replace(
    {
        "AO01": "A1: Expert knowledge",
        "AO02": "A2: Advanced knowledge",
        "AO03": "A3: Some knowledge",
        "AO04": "A4: Basic knowledge",
        "AO05": "A5: No knowledge",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
    }
)

df["expertise3"] = df["expertise3"].replace(
    {
        "AO01": "A1: Expert knowledge",
        "AO02": "A2: Advanced knowledge",
        "AO03": "A3: Some knowledge",
        "AO04": "A4: Basic knowledge",
        "AO05": "A5: No knowledge",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
    }
)

df["expertise4"] = df["expertise4"].replace(
    {
        "AO01": "A1: Expert knowledge",
        "AO02": "A2: Advanced knowledge",
        "AO03": "A3: Some knowledge",
        "AO04": "A4: Basic knowledge",
        "AO05": "A5: No knowledge",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
    }
)

df["finance1"] = df["finance1"].replace(
    {
        "AO01": "A1: A great deal of funding",
        "AO02": "A2: Sufficient funding",
        "AO03": "A3: Some funding",
        "AO04": "A4: Little funding",
        "AO05": "A5: No funding",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
    }
)

df["finance2ms"] = df["finance2ms"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
    }
)

finance2cs_options = [
    "private_foundations",
    "donations",
    "national_public_funds",
    "corporate_sponsorship",
    "international_public_funds",
    "other",
]
for label in finance2cs_options:
    df[f"finance2cs[{label}]"] = df[f"finance2cs[{label}]"].replace(
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

df["finance4"] = df["finance4"].replace(
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
        "AO01": "A1: Yes, within 30 days",
        "AO02": "A2: No, usually longer than 30 days",
        "AO03": "A3: Never",
        "AO04": "A4: I don't know",
        "AO05": "A5: I prefere not to say",
    }
)

df.loc[is_civsoc, "foi4"] = df["foi4"].replace(
    {
        "AO01": "A1: Very helpful",
        "AO03": "A2: Helpful in parts",
        "AO05": "A3: Not helpful at all",
        "AO06": "A4: I don't know",
        "AO07": "A5: I prefer not to say",
    }
)

df.loc[is_media, "foi4"] = df["foi4"].replace(
    {
        "AO01": "A1: Very helpful",
        "AO02": "A2: Helpful in parts",
        "AO03": "A3: Not helpful at all",
        "AO06": "A4: I don't know",
        "AO07": "A5: I prefer not to say",
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
        "AO01": "A1: I have full confidence that the right tools <br>will protect my communication from surveillance",
        "AO02": "A2: Technological tools help to protect my identity <br>to some extent, but an attacker with sufficient power <br>may eventually be able to bypass my technological <br>safeguards",
        "AO03": "A3: Under the current conditions of communications <br>surveillance, technological solutions cannot offer <br>sufficient protection for the data I handle",
        "AO04": "A4: I have no confidence in the protection offered by <br>technological tools",
        "AO05": "A5: I try to avoid technology-based communication whenever <br>possible when I work on intelligence-related issues",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
    }
)

df["protectleg1"] = df["protectleg1"].replace(
    {
        "AO01": "A1: Always",
        "AO02": "A2: Often",
        "AO03": "A3: Sometimes",
        "AO04": "A4: Rarely",
        "AO05": "A5: Never",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
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
        "AO01": "A1: Intelligence agencies are incompatible with<br>democratic values and should be abolished",
        "AO02": "A2: Intelligence agencies contradict democratic<br>principles, and their powers should be kept at a<br>bare minimum",
        "AO03": "A3: Intelligence agencies are necessary and<br>legitimate institutions of democratic states,<br>even though they may sometimes overstep their<br>legal mandates",
        "AO04": "A4: Intelligence agencies are a vital component<br>of national security and should be shielded from<br>excessive bureaucratic restrictions",
        "AO05": "A5: I prefer not to say",
    }
)

df["attitude2"] = df["attitude2"].replace(
    {
        "AO01": "A1: Intelligence oversight generally succeeds<br>in uncovering past misconduct and preventing<br>future misconduct",
        "AO02": "A2: Intelligence oversight is mostly effective,<br>however its institutional design needs reform<br>for oversight practitioners to reliably uncover<br>past misconduct and prevent future misconduct",
        "AO03": "A3: Intelligence oversight lacks efficacy,<br>hence a fundamental reorganization of oversight<br>capacity is needed for oversight practitioners<br>to reliably uncover past misconduct and prevent<br>future misconduct",
        "AO04": "A4: Effective intelligence oversight is a<br>hopeless endeavour and even a systematic<br>reorganization is unlikely to ensure misconduct<br>is uncovered and prevented.",
        "AO05": "A5: I prefer not to say",
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

# ===========================================================================
# Make answers analysable (change data types etc.)
# ===========================================================================

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
    if (
        col.startswith("foi5[")
        or col.startswith("attitude3")
        or col.startswith("hr3")
        or col.startswith("soc5")
        or col.startswith("soc6")
        or col.startswith("impact1")
        or col.startswith("impact2")
        or col.startswith("attitude3")
    ):
        df[col] = df[col].replace(np.nan, False)
        df[col] = df[col].replace("Y", True)
        df[col] = df[col].astype("bool")

# ===========================================================================
# Export data to file
# ===========================================================================

df.to_pickle("data/merged.pkl")
df.to_excel("data/merged.xlsx")
df.to_csv("data/merged.csv")

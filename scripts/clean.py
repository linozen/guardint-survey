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
            "CSfinance2[SQ01]": "CSCSfinance2[private_foundations]",
            "CSfinance2[SQ02]": "CSCSfinance2[donations]",
            "CSfinance2[SQ03]": "CSCSfinance2[national_public_funds]",
            "CSfinance2[SQ04]": "CSCSfinance2[corporate_sponsorship]",
            "CSfinance2[SQ05]": "CSCSfinance2[international_public_funds]",
            "CSfinance2[SQ06]": "CSCSfinance2[other]",
            "CSfoi5[SQ01]": "CSfoi5[not_aware]",
            "CSfoi5[SQ02]": "CSfoi5[not_covered]",
            "CSfoi5[SQ03]": "CSfoi5[too_expensive]",
            "CSfoi5[SQ04]": "CSfoi5[too_time_consuming]",
            "CSfoi5[SQ05]": "CSfoi5[afraid_of_data_destruction]",
            "CSfoi5[SQ06]": "CSfoi5[afraid_of_discrimination]",
            "CSfoi5[SQ07]": "CSfoi5[other]",
            "CSfoi5[SQ08]": "CSfoi5[dont_know]",
            "CSfoi5[SQ09]": "CSfoi5[prefer_not_to_say]",
            "CSpreselection": "CSCSpreselection",
            "CScampact2[SQ01]": "CSCScampact2[media_contributions]",
            "CScampact2[SQ02]": "CSCScampact2[own_publications]",
            "CScampact2[SQ03]": "CSCScampact2[petitions_open_letters]",
            "CScampact2[SQ04]": "CSCScampact2[public_events]",
            "CScampact2[SQ05]": "CSCScampact2[collaborations]",
            "CScampact2[SQ06]": "CSCScampact2[demonstrations]",
            "CScampact2[SQ07]": "CSCScampact2[social_media]",
            "CScampact2[SQ08]": "CSCScampact2[advertising]",
            "CScampact2[SQ09]": "CSCScampact2[volunteer_activities]",
            "CScampact2[SQ10]": "CSCScampact2[providing_technical_tools]",
            "CScampact2[SQ11]": "CSCScampact2[support_for_eu_campaigns]",
            "CScampact2[SQ12]": "CSCScampact2[other]",
            "CScampimpact1[SQ01]": "CSCScampimpact1[increased_awareness]",
            "CScampimpact1[SQ02]": "CSCScampimpact1[policies_reflect_demands]",
            "CScampimpact1[SQ03]": "CSCScampimpact1[created_media_attention]",
            "CScampimpact1[SQ04]": "CSCScampimpact1[achieved_goals]",
            "CScampimpact2": "CSCScampimpact2",
            "CScamptrans1": "CSCScamptrans1",
            "CScamptrans2": "CSCScamptrans2",
            "CSadvocact2[SQ01]": "CSCSadvocact2[research]",
            "CSadvocact2[SQ02]": "CSCSadvocact2[consultations]",
            "CSadvocact2[SQ03]": "CSCSadvocact2[briefings]",
            "CSadvocact2[SQ04]": "CSCSadvocact2[expert_events]",
            "CSadvocact2[SQ05]": "CSCSadvocact2[participation_in_fora]",
            "CSadvocact2[SQ06]": "CSCSadvocact2[legal_opinions]",
            "CSadvocact2[SQ07]": "CSCSadvocact2[informal_encounters]",
            "CSadvocact2[SQ08]": "CSCSadvocact2[other]",
            "CSadvoctrans1": "CSCSadvoctrans1",
            "CSadvoctrans2": "CSCSadvoctrans2",
            "CSadvocimpact1[SQ01]": "CSCSadvocimpact1[increased_awareness]",
            "CSadvocimpact1[SQ02]": "CSCSadvocimpact1[policies_reflect_recommendations]",
            "CSadvocimpact1[SQ03]": "CSCSadvocimpact1[more_informed_debates]",
            "CSadvocimpact1[SQ04]": "CSCSadvocimpact1[achieved_goals]",
            "CSlitigateact2[SQ01]": "CSCSlitigateact2[initiating_lawsuit]",
            "CSlitigateact2[SQ02]": "CSCSlitigateact2[initiating_complaint]",
            "CSlitigateact2[SQ03]": "CSCSlitigateact2[supporting_existing_legislation]",
            "CSlitigateact2[SQ04]": "CSCSlitigateact2[other]",
            "CSlitigateimpact1[SQ01]": "CSCSlitigateimpact1[increased_awareness]",
            "CSlitigateimpact1[SQ02]": "CSCSlitigateimpact1[changed_the_law]",
            "CSlitigateimpact1[SQ03]": "CSCSlitigateimpact1[amendments_of_the_law]",
            "CSlitigateimpact1[SQ04]": "CSCSlitigateimpact1[revealed_new_information]",
            "CSlitigateimpact1[SQ05]": "CSCSlitigateimpact1[achieved_goals]",
            "CSlitigateimpact2": "CSCSlitigateimpact2",
            "CSlitigatecost1": "CSCSlitigatecost1",
            "CSlitigatecost2": "CSCSlitigatecost2",
            "CSlitigatecost3": "CSCSlitigatecost3",
            "CSlitigatetrans1": "CSCSlitigatetrans1",
            "CSlitigatetrans2": "CSCSlitigatetrans2",
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
            "CSconstraintself1[SQ01]": "CSCSconstraintself1[avoid]",
            "CSconstraintself1[SQ02]": "CSCSconstraintself1[cancelled_campaign]",
            "CSconstraintself1[SQ03]": "CSCSconstraintself1[withdrew_litigation]",
            "CSconstraintself1[SQ04]": "CSCSconstraintself1[leave_profession]",
            "CSconstraintself1[SQ05]": "CSCSconstraintself1[other]",
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
            "CSCSfinance2[private_foundations]",
            "CSCSfinance2[donations]",
            "CSCSfinance2[national_public_funds]",
            "CSCSfinance2[corporate_sponsorship]",
            "CSCSfinance2[international_public_funds]",
            "CSCSfinance2[other]",
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
            "CSCSpreselection",
            "CSCScampact2[media_contributions]",
            "CSCScampact2[own_publications]",
            "CSCScampact2[petitions_open_letters]",
            "CSCScampact2[public_events]",
            "CSCScampact2[collaborations]",
            "CSCScampact2[demonstrations]",
            "CSCScampact2[social_media]",
            "CSCScampact2[advertising]",
            "CSCScampact2[volunteer_activities]",
            "CSCScampact2[providing_technical_tools]",
            "CSCScampact2[support_for_eu_campaigns]",
            "CSCScampact2[other]",
            "CSCScamptrans1",
            "CSCScamptrans2",
            "CSCScampimpact1[increased_awareness]",
            "CSCScampimpact1[policies_reflect_demands]",
            "CSCScampimpact1[created_media_attention]",
            "CSCScampimpact1[achieved_goals]",
            "CSCSadvoctrans1",
            "CSCSadvoctrans2",
            "CSCSadvocact2[research]",
            "CSCSadvocact2[consultations]",
            "CSCSadvocact2[briefings]",
            "CSCSadvocact2[expert_events]",
            "CSCSadvocact2[participation_in_fora]",
            "CSCSadvocact2[legal_opinions]",
            "CSCSadvocact2[informal_encounters]",
            "CSCSadvocact2[other]",
            "CSCSadvocimpact1[increased_awareness]",
            "CSCSadvocimpact1[policies_reflect_recommendations]",
            "CSCSadvocimpact1[more_informed_debates]",
            "CSCSadvocimpact1[achieved_goals]",
            "CSCSlitigateact2[initiating_lawsuit]",
            "CSCSlitigateact2[initiating_complaint]",
            "CSCSlitigateact2[supporting_existing_legislation]",
            "CSCSlitigateact2[other]",
            "CSCSlitigatecost1",
            "CSCSlitigatecost2",
            "CSCSlitigatecost3",
            "CSCSlitigatetrans1",
            "CSCSlitigatetrans2",
            "CSCSlitigateimpact1[increased_awareness]",
            "CSCSlitigateimpact1[changed_the_law]",
            "CSCSlitigateimpact1[amendments_of_the_law]",
            "CSCSlitigateimpact1[revealed_new_information]",
            "CSCSlitigateimpact1[achieved_goals]",
            "CSCSlitigateimpact2",
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
            "CSCSconstraintself1[avoid]",
            "CSCSconstraintself1[cancelled_campaign]",
            "CSCSconstraintself1[withdrew_litigation]",
            "CSCSconstraintself1[leave_profession]",
            "CSCSconstraintself1[other]",
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
            "MSfinance2": "MSMSfinance2",
            "MFfoi2": "MSfoi2",
            "MShr3[SQ01]": "MSMShr3[daily_newspaper]",
            "MShr3[SQ02]": "MSMShr3[weekly_newspaper]",
            "MShr3[SQ03]": "MSMShr3[magazine]",
            "MShr3[SQ04]": "MSMShr3[tv]",
            "MShr3[SQ05]": "MSMShr3[radio]",
            "MShr3[SQ06]": "MSMShr3[news_agency]",
            "MShr3[SQ07]": "MSMShr3[online_stand_alone]",
            "MShr3[SQ08]": "MSMShr3[online_of_offline]",
            "MShr4": "MSMShr4",
            "MSfoi5[SQ01]": "MSfoi5[not_aware]",
            "MSfoi5[SQ02]": "MSfoi5[not_covered]",
            "MSfoi5[SQ03]": "MSfoi5[too_expensive]",
            "MSfoi5[SQ04]": "MSfoi5[too_time_consuming]",
            "MSfoi5[SQ05]": "MSfoi5[afraid_of_data_destruction]",
            "MSfoi5[SQ06]": "MSfoi5[afraid_of_discrimination]",
            "MSfoi5[SQ07]": "MSfoi5[other]",
            "MSfoi5[SQ08]": "MSfoi5[dont_know]",
            "MSfoi5[SQ09]": "MSfoi5[prefer_not_to_say]",
            "MSapp1": "MSMSapp1",
            "MSapp2": "MSMSapp2",
            "MSsoc1": "MSMSsoc1",
            "MSsoc2": "MSMSsoc2",
            "MSsoc4": "MSMSsoc3",
            "MSsoc5[SQ01]": "MSMSsoc4[follow_up_on_other_media]",
            "MSsoc5[SQ02]": "MSMSsoc4[statements_government]",
            "MSsoc5[SQ03]": "MSMSsoc4[oversight_reports]",
            "MSsoc5[SQ04]": "MSMSsoc4[leaks]",
            "MSsoc5[SQ05]": "MSMSsoc4[own_investigations]",
            "MSsoc5[SQ07]": "MSMSsoc4[dont_know]",
            "MSsoc5[SQ08]": "MSMSsoc4[prefer_not_to_say]",
            "MSsoc5[SQ09]": "MSMSsoc4[other]",
            "MSsoc6[SQ01]": "MSMSsoc5[national_security_risks]",
            "MSsoc6[SQ02]": "MSMSsoc5[intelligence_success]",
            "MSsoc6[SQ03]": "MSMSsoc5[intelligence_misconduct]",
            "MSsoc6[SQ04]": "MSMSsoc5[oversight_interventions]",
            "MSsoc6[SQ05]": "MSMSsoc5[oversight_failures]",
            "MSsoc6[SQ06]": "MSMSsoc5[policy_debates_leg_reforms]",
            "MSsoc6[SQ07]": "MSMSsoc5[other]",
            "MStrans1": "MSMStrans1",
            "MStrans2": "MSMStrans2",
            "MStrans3": "MSMStrans3",
            "MSimpact1[SQ01]": "MSMSimpact1[above_avg_comments]",
            "MSimpact1[SQ02]": "MSMSimpact1[above_avg_shares]",
            "MSimpact1[SQ03]": "MSMSimpact1[above_avg_readers]",
            "MSimpact1[SQ04]": "MSMSimpact1[letters_to_the_editor]",
            "MSimpact1[SQ05]": "MSMSimpact1[follow_up_by_other_media]",
            "MSimpact1[SQ06]": "MSMSimpact1[other]",
            "MSimpact1[SQ07]": "MSMSimpact1[none_of_the_above]",
            "MSimpact1[SQ08]": "MSMSimpact1[dont_know]",
            "MSimpact1[SQ09]": "MSMSimpact1[prefer_not_to_say]",
            "MSimpact2[SQ01]": "MSMSimpact2[diplomatic_pressure]",
            "MSimpact2[SQ02]": "MSMSimpact2[civic_action]",
            "MSimpact2[SQ03]": "MSMSimpact2[conversations_with_government]",
            "MSimpact2[SQ04]": "MSMSimpact2[official_inquiries]",
            "MSimpact2[SQ05]": "MSMSimpact2[government_statements]",
            "MSimpact2[SQ06]": "MSMSimpact2[conversations_with_intelligence]",
            "MSimpact2[SQ08]": "MSMSimpact2[dont_know]",
            "MSimpact2[SQ09]": "MSMSimpact2[prefer_not_to_say]",
            "MSimpact2[SQ10]": "MSMSimpact2[other]",
            "MSimpact2[SQ11]": "MSMSimpact2[none_of_the_above]",
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
            "MSprotectops3[SQ07]": "MSprotectops3[secure_drop]",
            "MSprotectops3[SQ08]": "MSprotectops3[other]",
            "MSprotectleg3[SQ01]": "MSprotectleg3[free_counsel]",
            "MSprotectleg3[SQ02]": "MSprotectleg3[cost_insurance]",
            "MSprotectleg3[SQ03]": "MSprotectleg3[other]",
            "MSprotectrta1": "MSMSprotectrta1",
            "MSprotectrta2": "MSMSprotectrta2",
            "MSprotectrta3": "MSMSprotectrta3",
            "MSprotectrta4": "MSMSprotectrta4",
            "MSprotectrta5": "MSMSprotectrta5",
            "MSprotectrta6": "MSMSprotectrta6",
            "MSconstraintcen1": "MSMSconstraintcen1",
            "MSconstraintcen2": "MSMSconstraintcen2",
            "MSconstraintcen3": "MSMSconstraintcen3",
            "MSconstraintcen4": "MSMSconstraintcen4",
            "MSconstraintcen5": "MSMSconstraintcen5",
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
            "MSconstraintself1[SQ01]": "MSMSconstraintself1[avoid]",
            "MSconstraintself1[SQ02]": "MSMSconstraintself1[change_focus]",
            "MSconstraintself1[SQ03]": "MSMSconstraintself1[change_timeline]",
            "MSconstraintself1[SQ04]": "MSMSconstraintself1[abandon]",
            "MSconstraintself1[SQ05]": "MSMSconstraintself1[leave_profession]",
            "MSconstraintself1[SQ06]": "MSMSconstraintself1[other]",
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
            "MSMShr3[daily_newspaper]",
            "MSMShr3[weekly_newspaper]",
            "MSMShr3[magazine]",
            "MSMShr3[tv]",
            "MSMShr3[radio]",
            "MSMShr3[news_agency]",
            "MSMShr3[online_stand_alone]",
            "MSMShr3[online_of_offline]",
            "MSMShr4",
            "MSgender",
            "MSexpertise1",
            "MSexpertise2",
            "MSexpertise3",
            "MSexpertise4",
            "MSfinance1",
            "MSMSfinance2",
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
            "MSMSapp1",
            "MSMSapp2",
            "MSMSsoc1",
            "MSMSsoc2",
            "MSMSsoc3",
            "MSMSsoc4[follow_up_on_other_media]",
            "MSMSsoc4[statements_government]",
            "MSMSsoc4[oversight_reports]",
            "MSMSsoc4[leaks]",
            "MSMSsoc4[own_investigations]",
            "MSMSsoc4[dont_know]",
            "MSMSsoc4[prefer_not_to_say]",
            "MSMSsoc4[other]",
            "MSMSsoc5[national_security_risks]",
            "MSMSsoc5[intelligence_success]",
            "MSMSsoc5[intelligence_misconduct]",
            "MSMSsoc5[oversight_interventions]",
            "MSMSsoc5[oversight_failures]",
            "MSMSsoc5[policy_debates_leg_reforms]",
            "MSMSsoc5[other]",
            "MSMStrans1",
            "MSMStrans2",
            "MSMStrans3",
            "MSMSimpact1[above_avg_comments]",
            "MSMSimpact1[above_avg_shares]",
            "MSMSimpact1[above_avg_readers]",
            "MSMSimpact1[letters_to_the_editor]",
            "MSMSimpact1[follow_up_by_other_media]",
            "MSMSimpact1[other]",
            "MSMSimpact1[none_of_the_above]",
            "MSMSimpact1[dont_know]",
            "MSMSimpact1[prefer_not_to_say]",
            "MSMSimpact2[diplomatic_pressure]",
            "MSMSimpact2[civic_action]",
            "MSMSimpact2[conversations_with_government]",
            "MSMSimpact2[official_inquiries]",
            "MSMSimpact2[government_statements]",
            "MSMSimpact2[conversations_with_intelligence]",
            "MSMSimpact2[dont_know]",
            "MSMSimpact2[prefer_not_to_say]",
            "MSMSimpact2[other]",
            "MSprotectops1[sectraining]",
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
            "MSprotectops4",
            "MSprotectleg1",
            "MSprotectleg2",
            "MSprotectleg3[free_counsel]",
            "MSprotectleg3[cost_insurance]",
            "MSprotectleg3[other]",
            "MSMSprotectrta1",
            "MSMSprotectrta2",
            "MSMSprotectrta3",
            "MSMSprotectrta4",
            "MSMSprotectrta5",
            "MSMSprotectrta6",
            "MSMSconstraintcen1",
            "MSMSconstraintcen2",
            "MSMSconstraintcen3",
            "MSMSconstraintcen4",
            "MSMSconstraintcen5",
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
            "MSMSconstraintself1[avoid]",
            "MSMSconstraintself1[change_focus]",
            "MSMSconstraintself1[change_timeline]",
            "MSMSconstraintself1[abandon]",
            "MSMSconstraintself1[leave_profession]",
            "MSMSconstraintself1[other]",
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
    df["field"] = "Journalists"
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
is_media = df.field == "Journalists"
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

df["MShr4"] = df["MShr4"].replace(
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

df["MSfinance2"] = df["MSfinance2"].replace(
    {
        "AO01": "Yes",
        "AO02": "No",
        "AO03": "I don't know",
        "AO04": "I prefer not to say",
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

df["MStrans1"] = df["MStrans1"].replace(
    {
        "AO001": "A1: Always",
        "AO002": "A2: Often (75% of the time)",
        "AO003": "A3: Sometimes (50% of the time)",
        "AO004": "A4: Rarely (25% of the time)",
        "AO005": "A5: Never",
        "AO006": "A6: I don't know",
        "AO007": "A7: I prefer not to say",
    }
)

df["MStrans2"] = df["MStrans2"].replace(
    {
        "AO01": "A1: Always",
        "AO02": "A2: Often (75% of the time)",
        "AO03": "A3: Sometimes (50% of the time)",
        "AO04": "A4: Rarely (25% of the time)",
        "AO05": "A5: Never",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
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
        "AO01": "A1: Always",
        "AO02": "A2: Often (75% of the time)",
        "AO03": "A3: Sometimes (50% of the time)",
        "AO04": "A4: Rarely (25% of the time)",
        "AO05": "A5: Never",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
    }
)

df["CScamptrans2"] = df["CScamptrans2"].replace(
    {
        "AO01": "A1: Always",
        "AO02": "A2: Often (75% of the time)",
        "AO03": "A3: Sometimes (50% of the time)",
        "AO04": "A4: Rarely (25% of the time)",
        "AO05": "A5: Never",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
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
        "AO01": "A1: Always",
        "AO02": "A2: Often (75% of the time)",
        "AO03": "A3: Sometimes (50% of the time)",
        "AO04": "A4: Rarely (25% of the time)",
        "AO05": "A5: Never",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
    }
)

df["CSadvoctrans2"] = df["CSadvoctrans2"].replace(
    {
        "AO01": "A1: Always",
        "AO02": "A2: Often (75% of the time)",
        "AO03": "A3: Sometimes (50% of the time)",
        "AO04": "A4: Rarely (25% of the time)",
        "AO05": "A5: Never",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
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
        "AO01": "A1: Always",
        "AO02": "A2: Often (75% of the time)",
        "AO03": "A3: Sometimes (50% of the time)",
        "AO04": "A4: Rarely (25% of the time)",
        "AO05": "A5: Never",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
    }
)

df["CSlitigatetrans2"] = df["CSlitigatetrans2"].replace(
    {
        "AO01": "A1: Always",
        "AO02": "A2: Often (75% of the time)",
        "AO03": "A3: Sometimes (50% of the time)",
        "AO04": "A4: Rarely (25% of the time)",
        "AO05": "A5: Never",
        "AO06": "A6: I don't know",
        "AO07": "A7: I prefer not to say",
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
            "AO01": "A1: Always or very often",
            "AO02": "A2: Often (75% of the time)",
            "AO03": "A3: Sometimes (50% of the time)",
            "AO04": "A4: Rarely (25% of the time)",
            "AO05": "A5: Never or rarely",
            "AO06": "A6: I don't know",
            "AO07": "A7: I prefer not to say",
        }
    )

df["CSlitigatecost3"] = df["CSlitigatecost3"].replace(
    {
        "AO01": "A1: Not risky at all",
        "AO02": "A2: Somewaht risky",
        "AO03": "A3: Very risky",
        "AO04": "A4: I don't know",
        "AO05": "A5: I prefer not to say",
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
    "secure_drop",
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
            "AO01": "A1: Very important",
            "AO02": "A2: Important",
            "AO03": "A3: Somewhat important",
            "AO04": "A4: Slightly important",
            "AO05": "A5: Not important at all",
            # notice the AO09 instead of AO06 as above
            "AO09": "A6: I don't know",
            "AO11": "A7: I prefer not to say",
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
        or col.startswith("MShr3")
        or col.startswith("MSsoc4")
        or col.startswith("MSsoc5")
        or col.startswith("MSimpact1")
        or col.startswith("MSimpact2")
        or col.startswith("attitude3")
    ):
        df[col] = df[col].replace(np.nan, False)
        df[col] = df[col].replace("Y", True)
        df[col] = df[col].astype("bool")

# ===========================================================================
# Export data to file
# ===========================================================================

df.to_pickle("data/guardint_survey.pkl")
df.to_excel("data/guardint_survey.xlsx")
df.to_csv("data/guardint_survey.csv")

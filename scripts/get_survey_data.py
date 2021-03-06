#!/usr/bin/env python3

"""Use the LS RemoteControl 2 API to download survey data
Based on: https://manual.limesurvey.org/RemoteControl_2_API
Documentation: https://api.limesurvey.org/classes/remotecontrol_handle.html
"""

import configparser
from pathlib import Path
import base64
import requests

ENDPOINT = "{}/index.php/admin/remotecontrol"


def get_session_key(base_url, user_name, password, user_id):
    """Get session key"""

    api_url = ENDPOINT.format(base_url)
    payload = {
        "method": "get_session_key",
        "params": [user_name, password],
        "id": user_id,
    }
    req = requests.post(api_url, json=payload)
    return req.json()


def export_responses(
    user_id,
    base_url,
    session_key,
    sid,
    lang=None,
    document_type="csv",
    completion_status="all",
    heading_type="code",
    response_type="short",
    from_response_id=None,
    to_response_id=None,
    fields=None,
):
    """Export responses"""

    api_url = ENDPOINT.format(base_url)
    payload = {
        "method": "export_responses",
        "params": [
            session_key,
            sid,
            document_type,
            lang,
            completion_status,
            heading_type,
            response_type,
            from_response_id,
            to_response_id,
            fields,
        ],
        "id": user_id,
    }
    req = requests.post(api_url, json=payload)
    result = req.json()["result"]
    if "status" in result:
        raise ValueError(result["status"])
    csv = base64.b64decode(result.encode()).decode("utf-8-sig")
    return csv


def release_session_key(base_url, session_key, user_id):
    """Release session key"""

    api_url = ENDPOINT.format(base_url)
    payload = {"method": "release_session_key", "params": [session_key], "id": user_id}
    req = requests.post(api_url, json=payload)
    return req.json()["result"]


def get_responses(
    base_url,
    user_name,
    password,
    user_id,
    sid,
    lang=None,
    document_type="csv",
    completion_status="all",
    heading_type="code",
    response_type="short",
    from_response_id=None,
    to_response_id=None,
    fields=None,
):
    """Get session key, download and store responses and close session.

    :param base_url: e.g. https://mywebsite.nl/survey.
    :param user_name: LimeSurvey user name
    :param password: LimeSurvey user password
    :param user_id: LimeSurvey user id
    :param sid: LimeSurvey survey id
    :param lang: language. (Default value = None)
    :param document_type: format for results (Default value = 'csv')
    :param completion_status: which responses to export, 'complete',
        'incomplete' or 'all' (Default value = 'all')
    :param heading_type: 'code', 'full' or 'abbreviated'
        (Default value = 'code')
    :param response_type: 'short' or 'long' (Default value = 'short')
    :param from_response_id: for partial export (Default value = None)
    :param to_response_id: for partial export (Default value = None)
    :param fields: for partial export (Default value = None)

    """
    session_key = get_session_key(base_url, user_name, password, user_id)
    session_key = session_key["result"]
    csv = export_responses(
        user_id,
        base_url,
        session_key,
        sid,
        lang,
        document_type,
        completion_status,
        heading_type,
        response_type,
        from_response_id,
        to_response_id,
        fields,
    )
    release_session_key(base_url, session_key, user_id)
    return csv


def get_survey_data_long(survey_id: str, survey_name: str):
    """Get the surveys as DataFrame for the IDs specified.

    Keyword arguemnts:
    survey_id   -- survey ID found on limesurvey
    survey_name -- name under which the .csv should be saved
    """
    config = configparser.ConfigParser()
    config.read("scripts/config.ini")
    url = config["limesurvey"]["url"]
    username = config["limesurvey"]["username"]
    uid = config["limesurvey"]["uid"]
    password = config["limesurvey"]["password"]
    csv = get_responses(url, username, password, uid, survey_id, response_type="long")
    path = Path(f"data/limesurvey/{survey_name}.csv")
    path.write_text(csv)


get_survey_data_long("274185", "cs_uk_long")
get_survey_data_long("629424", "cs_de_long")
get_survey_data_long("151418", "cs_fr_long")
get_survey_data_long("775898", "ms_uk_long")
get_survey_data_long("694698", "ms_de_long")
get_survey_data_long("264469", "ms_fr_long")


def get_survey_data_short(survey_id: str, survey_name: str):
    """Get the surveys as DataFrame for the IDs specified.

    Keyword arguemnts:
    survey_id   -- survey ID found on limesurvey
    survey_name -- name under which the .csv should be saved
    """
    config = configparser.ConfigParser()
    config.read("scripts/config.ini")
    url = config["limesurvey"]["url"]
    username = config["limesurvey"]["username"]
    uid = config["limesurvey"]["uid"]
    password = config["limesurvey"]["password"]
    csv = get_responses(url, username, password, uid, survey_id, response_type="short")
    path = Path(f"data/limesurvey/{survey_name}.csv")
    path.write_text(csv)


get_survey_data_short("274185", "cs_uk_short")
get_survey_data_short("629424", "cs_de_short")
get_survey_data_short("151418", "cs_fr_short")
get_survey_data_short("775898", "ms_uk_short")
get_survey_data_short("694698", "ms_de_short")
get_survey_data_short("264469", "ms_fr_short")

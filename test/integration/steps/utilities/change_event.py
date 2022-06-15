from datetime import datetime
import re
from dateutil.relativedelta import relativedelta
from json import load
from typing import Dict, Any
from .utils import (
    get_change_event_demographics,
    get_change_event_specified_opening_times,
    get_change_event_standard_opening_times,
    get_single_service_pharmacy,
    random_dentist_odscode,
    random_pharmacy_odscode,
)
from .constants import PHARMACY_ORG_TYPE_ID, DENTIST_ORG_TYPE_ID, PHARMACY_SUB_TYPE, DENTIST_SUB_TYPE


def create_change_event(service_type: str) -> Dict[str, Any]:
    with open("resources/payloads/expected_schema.json", "r", encoding="utf-8") as json_file:
        payload = load(json_file)
        match service_type.upper():
            case "PHARMACY":
                payload["ODSCode"] = random_pharmacy_odscode()
            case "DENTIST":
                payload["ODSCode"] = random_dentist_odscode()
            case _:
                raise ValueError(f"Service type {service_type} does not exist")
        payload["OrganisationName"] = f'{payload["OrganisationName"]} {datetime.now()}'
        print(payload["ODSCode"])
        return payload


def build_same_as_dos_change_event_by_ods(service_type: str, ods_code: str):
    change_event = create_change_event(service_type)
    match service_type.upper():
        case "PHARMACY":
            change_event["ODSCode"] = ods_code
            demographics_data = get_change_event_demographics(change_event["ODSCode"], PHARMACY_ORG_TYPE_ID)
            org_type_id = PHARMACY_ORG_TYPE_ID
            org_sub_type = PHARMACY_SUB_TYPE
        case "DENTIST":
            change_event["ODSCode"] = ods_code
            demographics_data = get_change_event_demographics(change_event["ODSCode"], DENTIST_ORG_TYPE_ID)
            org_type_id = DENTIST_ORG_TYPE_ID
            org_sub_type = DENTIST_SUB_TYPE
        case _:
            raise ValueError(f"Service type {service_type} does not exist")
    print(f"Latest selected ODSCode: {change_event['ODSCode']}")
    change_event["OrganisationTypeId"] = org_type_id
    change_event["OrganisationSubType"] = org_sub_type
    change_event["OrganisationName"] = demographics_data["publicname"]
    change_event["Postcode"] = demographics_data["postcode"]
    change_event["Contacts"][0]["ContactValue"] = demographics_data["web"]
    change_event["Contacts"][1]["ContactValue"] = demographics_data["publicphone"]
    address_keys = ["Address1", "Address2", "Address3", "City", "County"]
    for address_key in address_keys:
        change_event[address_key] = None
    address_parts = demographics_data["address"].split("$", 4)
    counter = 0
    for address_part in address_parts:
        change_event[address_keys[counter]] = address_part
        counter += 1
    standard_opening_times = get_change_event_standard_opening_times(demographics_data["id"])
    change_event["OpeningTimes"] = []
    for day in standard_opening_times:
        for opening_times in standard_opening_times[day]:
            change_event["OpeningTimes"].append(
                {
                    "Weekday": day,
                    "OpeningTime": opening_times["start_time"],
                    "ClosingTime": opening_times["end_time"],
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                }
            )
    specified_opening_times = get_change_event_specified_opening_times(demographics_data["id"])
    for date in specified_opening_times:
        for opening_times in specified_opening_times[date]:
            str_date = datetime.strptime(date, "%Y-%m-%d")
            change_event["OpeningTimes"].append(
                {
                    "Weekday": "",
                    "OpeningTime": opening_times["start_time"],
                    "ClosingTime": opening_times["end_time"],
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": str_date.strftime("%b %d %Y"),
                    "IsOpen": True,
                }
            )
    return change_event


def build_same_as_dos_change_event(service_type: str):
    match service_type.upper():
        case "DENTIST":
            ods_code = random_dentist_odscode()
        case "PHARMACY":
            ods_code = get_single_service_pharmacy()
        case _:
            raise ValueError(f"Service type {service_type} does not exist")
    change_event = build_same_as_dos_change_event_by_ods(service_type, ods_code)
    if valid_change_event(change_event):
        return change_event
    else:
        return build_same_as_dos_change_event(service_type)


def valid_change_event(change_event: dict) -> bool:
    """This function checks if the data stored in DoS would pass the change request
    validation within DoS API Gateway"""
    if not re.fullmatch(
        r"(https?:\/\/)?([a-z\d][a-z\d-]*[a-z\d]\.)+[a-z]{2,}(\/.*)?", str(change_event["Contacts"][0]["ContactValue"])
    ):  # Website
        return False
    if not re.fullmatch(r"[+0][0-9 ()]{9,}", str(change_event["Contacts"][1]["ContactValue"])):  # Phone
        return False
    return True


def set_opening_times_change_event(service_type: str):
    change_event = build_same_as_dos_change_event(service_type)
    date = datetime.today() + relativedelta(months=1)
    has_set_closed_day = False
    for day in change_event["OpeningTimes"]:
        if day["IsOpen"] and day["OpeningTimeType"] == "General":
            closed_day = day["Weekday"]
            has_set_closed_day = True
            break
    if has_set_closed_day is False:
        raise ValueError("ERROR!.. Unable to find 'Open' Standard opening time")
    change_event["OpeningTimes"] = list(filter(lambda day: day["Weekday"] != closed_day, change_event["OpeningTimes"]))
    change_event["OpeningTimes"].append(
        {
            "Weekday": closed_day,
            "OpeningTime": "",
            "ClosingTime": "",
            "Times": "-",
            "OffsetOpeningTime": 0,
            "OffsetClosingTime": 0,
            "OpeningTimeType": "General",
            "AdditionalOpeningDate": "",
            "IsOpen": False,
        }
    )
    change_event["OpeningTimes"].append(
        {
            "Weekday": "",
            "OpeningTime": "",
            "ClosingTime": "",
            "Times": "-",
            "OffsetOpeningTime": 0,
            "OffsetClosingTime": 0,
            "OpeningTimeType": "Additional",
            "AdditionalOpeningDate": date.strftime("%b %d %Y"),
            "IsOpen": False,
        }
    )
    return change_event

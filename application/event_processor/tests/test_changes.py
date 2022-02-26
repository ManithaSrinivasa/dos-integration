from unittest.mock import patch

from dos import dos_location_cache

from ..change_request import (
    ADDRESS_CHANGE_KEY,
    ADDRESS_LINES_KEY,
    OPENING_DATES_KEY,
    OPENING_DAYS_KEY,
    PHONE_CHANGE_KEY,
    POSTCODE_CHANGE_KEY,
    PUBLICNAME_CHANGE_KEY,
    WEBSITE_CHANGE_KEY,
)
from ..changes import (
    get_changes,
    update_changes,
    update_changes_with_address,
    update_changes_with_opening_times,
    update_changes_with_postcode,
)
from ..nhs import NHSEntity
from .conftest import dummy_dos_location, dummy_dos_service

FILE_PATH = "application.event_processor.changes"


def test_get_changes_same_data():
    # Act
    dos_service = dummy_dos_service()
    nhs_entity = NHSEntity(
        {
            "Postcode": dos_service.postcode,
            "Phone": dos_service.publicphone,
            "OrganisationName": dos_service.publicname,
            "Address1": dos_service.address,
            "Contacts": [
                {
                    "ContactType": "Primary",
                    "ContactAvailabilityType": "Office hours",
                    "ContactMethodType": "Website",
                    "ContactValue": dos_service.web,
                },
                {
                    "ContactType": "Primary",
                    "ContactAvailabilityType": "Office hours",
                    "ContactMethodType": "Telephone",
                    "ContactValue": dos_service.publicphone,
                },
            ],
            "OpeningTimes": [],
        }
    )
    # Act
    response = get_changes(dos_service, nhs_entity)
    # Assert
    assert {} == response, f"Should return empty dict, actually: {response}"


def test_get_changes_different_changes():
    # Arrange
    website = "changed-website.com"
    postcode = "TA1 TA1"
    phone = "0123456789"
    organisation_name = "changed-organisation-name"
    address1 = "changed-address1"
    address2 = "changed-address2"
    address3 = "changed-address3"
    city = "changed-city"
    county = "changed-county"

    nhs_entity = NHSEntity(
        {
            "Postcode": postcode,
            "OrganisationName": organisation_name,
            "Address1": address1,
            "Address2": address2,
            "Address3": address3,
            "City": city,
            "County": county,
            "Contacts": [
                {
                    "ContactType": "Primary",
                    "ContactAvailabilityType": "Office hours",
                    "ContactMethodType": "Website",
                    "ContactValue": website,
                },
                {
                    "ContactType": "Primary",
                    "ContactAvailabilityType": "Office hours",
                    "ContactMethodType": "Telephone",
                    "ContactValue": phone,
                },
            ],
            "OpeningTimes": [],
        }
    )

    dos_service = dummy_dos_service()
    dos_location = dummy_dos_location()
    dos_location.postcode = postcode
    dos_location_cache[dos_location.normal_postcode()] = [dos_location]

    expected_changes = {
        ADDRESS_CHANGE_KEY: {
            ADDRESS_LINES_KEY: [address1, address2, address3, city, county],
            POSTCODE_CHANGE_KEY: nhs_entity.postcode,
        },
        PUBLICNAME_CHANGE_KEY: organisation_name,
        WEBSITE_CHANGE_KEY: website,
        PHONE_CHANGE_KEY: phone,
    }
    # Act
    response = get_changes(dos_service, nhs_entity)
    # Assert
    assert expected_changes == response, f"Should return {expected_changes} dict, actually: {response}"


def test_update_changes_publicphone_to_change_request_if_not_equal_is_equal():
    # Arrange
    changes = {}
    # Act
    update_changes(changes, PHONE_CHANGE_KEY, "000000000", "000000000")
    update_changes(changes, PUBLICNAME_CHANGE_KEY, "boots", "boots")
    update_changes(changes, WEBSITE_CHANGE_KEY, "www.wow.co.uk", "www.wow.co.uk")
    # Assert
    assert changes == {}, f"Should return empty dict, actually: {changes}"


def test_update_changes_publicphone_to_change_request_if_not_equal_not_equal():
    # Arrange
    changes = {}
    nhs_uk_phone = "000000000"
    dos_public_phone = "123456789"
    expected_changes = {"publicphone": nhs_uk_phone}
    # Act
    update_changes(changes, "publicphone", dos_public_phone, nhs_uk_phone)
    # Assert
    assert changes == expected_changes, f"Should return {expected_changes} dict, actually: {changes}"


def test_update_changes_address_to_change_request_if_not_equal_is_equal():
    # Arrange
    changes = {}

    nhs_uk_entity = NHSEntity({})
    nhs_uk_entity.address_lines = ["address1" "address2" "address3" "city" "county"]

    dos_service = dummy_dos_service()
    dos_service.address = "$".join(nhs_uk_entity.address_lines)
    # Act
    actual_changes = update_changes_with_address(changes, dos_service, nhs_uk_entity)
    # Assert
    assert changes == actual_changes, f"Should return {changes} dict, actually: {actual_changes}"


def test_update_changes_address_to_change_request_if_not_equal_not_equal():
    # Arrange
    nhs_uk_entity = NHSEntity({})
    nhs_uk_entity.address_lines = ["address1", "address2", "address3", "city", "county"]

    dos_service = dummy_dos_service()
    dos_service.address = "Test RD$Testown$Testshire"

    # Act
    actual_changes = {}
    update_changes_with_address(actual_changes, dos_service, nhs_uk_entity)
    expected_changes = {ADDRESS_CHANGE_KEY: {ADDRESS_LINES_KEY: nhs_uk_entity.address_lines}}
    # Assert
    assert actual_changes == expected_changes, f"Should return {expected_changes} dict, actually: {actual_changes}"


@patch(f"{FILE_PATH}.get_valid_dos_postcode")
def test_do_not_update_address_if_postcode_invalid(mock_get_valid_dos_postcode, change_event):
    # Arrange
    nhs_entity = NHSEntity(change_event)
    dos_service = dummy_dos_service()
    mock_get_valid_dos_postcode.return_value = None
    existing_changes = {ADDRESS_CHANGE_KEY: ["address1", "address2", "address3", "city", "county"]}
    # Act
    update_changes_with_postcode(existing_changes, dos_service, nhs_entity)
    # Assert
    mock_get_valid_dos_postcode.assert_called_once_with(nhs_entity.normal_postcode())
    assert existing_changes == {}, f"Should return empty dict, actually: {existing_changes}"


@patch(f"{FILE_PATH}.get_valid_dos_postcode")
def test_do_not_update_address_if_postcode_invalid_no_address(mock_get_valid_dos_postcode, change_event):
    # Arrange
    nhs_entity = NHSEntity(change_event)
    dos_service = dummy_dos_service()
    mock_get_valid_dos_postcode.return_value = None
    existing_changes = {}
    # Act
    update_changes_with_postcode(existing_changes, dos_service, nhs_entity)
    # Assert
    mock_get_valid_dos_postcode.assert_called_once_with(nhs_entity.normal_postcode())
    assert existing_changes == {}, f"Should return empty dict, actually: {existing_changes}"


def test_update_changes_with_opening_times():
    # Arrange
    nhs_uk_entity = NHSEntity(
        {
            "OpeningTimes": [
                {
                    "Weekday": "Monday",
                    "OpeningTime": "09:00",
                    "ClosingTime": "12:00",
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
                {
                    "Weekday": "Monday",
                    "OpeningTime": "13:00",
                    "ClosingTime": "16:00",
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
                {
                    "Weekday": "Monday",
                    "OpeningTime": "17:00",
                    "ClosingTime": "18:00",
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
                {
                    "Weekday": "Tuesday",
                    "OpeningTime": "09:00",
                    "ClosingTime": "20:00",
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
                {
                    "Weekday": "Wednesday",
                    "OpeningTime": "09:00",
                    "ClosingTime": "20:00",
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
                {
                    "Weekday": "Thursday",
                    "OpeningTime": "09:00",
                    "ClosingTime": "20:00",
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
                {
                    "Weekday": "Friday",
                    "OpeningTime": "09:00",
                    "ClosingTime": "20:00",
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
                {
                    "Weekday": "Saturday",
                    "OpeningTime": "09:00",
                    "ClosingTime": "12:00",
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
                {
                    "Weekday": "Saturday",
                    "OpeningTime": "13:00",
                    "ClosingTime": "18:00",
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
                {
                    "Weekday": "Sunday",
                    "OpeningTime": None,
                    "ClosingTime": None,
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": False,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "08:00",
                    "ClosingTime": "12:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Apr 15 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "13:00",
                    "ClosingTime": "16:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Apr 15 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "07:00",
                    "ClosingTime": "11:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Apr 18 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "12:00",
                    "ClosingTime": "15:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Apr 18 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "16:00",
                    "ClosingTime": "18:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Apr 18 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": None,
                    "ClosingTime": None,
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Feb 21 2022",
                    "IsOpen": False,
                },
                {
                    "Weekday": "",
                    "OpeningTime": None,
                    "ClosingTime": None,
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Mar 7 2022",
                    "IsOpen": False,
                },
                {
                    "Weekday": "",
                    "OpeningTime": None,
                    "ClosingTime": None,
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Mar 8 2022",
                    "IsOpen": False,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "07:00",
                    "ClosingTime": "12:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Mar 10 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "13:00",
                    "ClosingTime": "17:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Mar 10 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "18:00",
                    "ClosingTime": "20:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Mar 10 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "07:00",
                    "ClosingTime": "12:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Mar 11 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "13:00",
                    "ClosingTime": "17:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Mar 11 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "18:00",
                    "ClosingTime": "20:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Mar 11 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "06:00",
                    "ClosingTime": "12:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Mar 19 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": "13:00",
                    "ClosingTime": "18:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Mar 19 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "OpeningTime": None,
                    "ClosingTime": None,
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Mar 9 2022",
                    "IsOpen": False,
                },
            ],
        }
    )

    expected_changes = {
        OPENING_DATES_KEY: {
            "2022-04-15": [{"start_time": "08:00", "end_time": "12:00"}, {"start_time": "13:00", "end_time": "16:00"}],
            "2022-04-18": [
                {"start_time": "07:00", "end_time": "11:00"},
                {"start_time": "12:00", "end_time": "15:00"},
                {"start_time": "16:00", "end_time": "18:00"},
            ],
            "2022-02-21": [],
            "2022-03-07": [],
            "2022-03-08": [],
            "2022-03-10": [
                {"start_time": "07:00", "end_time": "12:00"},
                {"start_time": "13:00", "end_time": "17:00"},
                {"start_time": "18:00", "end_time": "20:00"},
            ],
            "2022-03-11": [
                {"start_time": "07:00", "end_time": "12:00"},
                {"start_time": "13:00", "end_time": "17:00"},
                {"start_time": "18:00", "end_time": "20:00"},
            ],
            "2022-03-19": [{"start_time": "06:00", "end_time": "12:00"}, {"start_time": "13:00", "end_time": "18:00"}],
            "2022-03-09": [],
        },
        OPENING_DAYS_KEY: {
            "Monday": [
                {"start_time": "09:00", "end_time": "12:00"},
                {"start_time": "13:00", "end_time": "16:00"},
                {"start_time": "17:00", "end_time": "18:00"},
            ],
            "Tuesday": [{"start_time": "09:00", "end_time": "20:00"}],
            "Wednesday": [{"start_time": "09:00", "end_time": "20:00"}],
            "Thursday": [{"start_time": "09:00", "end_time": "20:00"}],
            "Friday": [{"start_time": "09:00", "end_time": "20:00"}],
            "Saturday": [{"start_time": "09:00", "end_time": "12:00"}, {"start_time": "13:00", "end_time": "18:00"}],
            "Sunday": [],
        },
    }
    dos_service = dummy_dos_service()
    # Act
    changes = {}
    update_changes_with_opening_times(changes, dos_service, nhs_uk_entity)
    print(changes)
    # Assert
    assert expected_changes == changes, f"Should return {expected_changes} dict, actually: {changes}"

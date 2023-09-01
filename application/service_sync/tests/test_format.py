import pytest

from application.service_sync.format import format_address, format_website


@pytest.mark.parametrize(
    ("address", "formatted_address"),
    [
        ("3rd Floor", "3Rd Floor"),
        ("24 Hour Road", "24 Hour Road"),
        ("Green Tye", "Green Tye"),
        ("Much Hadham", "Much Hadham"),
        ("Herts", "Herts"),
        ("24 hour road", "24 Hour Road"),
        ("green tye & woodsham", "Green Tye and Woodsham"),
        ("much hadham", "Much Hadham"),
        ("county", "County"),
        ("32A unit", "32A Unit"),
        ("george's road", "Georges Road"),
        ("green tye", "Green Tye"),
        ("less hadham", "Less Hadham"),
        ("testerset", "Testerset"),
        ("ABCDE", "Abcde"),
        ("WOODCHURCH ROAD", "Woodchurch Road"),
        ("TESTERSHIRE", "Testershire"),
    ],
)
def test_format_address(address: str, formatted_address: str):
    assert formatted_address == format_address(address)


@pytest.mark.parametrize(
    ("website", "formatted_website"),
    [
        ("www.test.com", "www.test.com"),
        ("www.Test.com", "www.test.com"),
        ("www.test.com/", "www.test.com/"),
        ("www.TEST.Com", "www.test.com"),
        ("www.Test.com/TEST", "www.test.com/TEST"),
        ("www.rowlandspharmacy.co.uk/test?foo=test", "www.rowlandspharmacy.co.uk/test?foo=test"),
        ("https://www.Test.com", "https://www.test.com"),
        ("https://www.test.com/", "https://www.test.com/"),
        ("https://www.TEST.Com", "https://www.test.com"),
        ("https://www.Test.com/TEST", "https://www.test.com/TEST"),
        ("https://www.rowlandspharmacy.co.uk/test?foo=test", "https://www.rowlandspharmacy.co.uk/test?foo=test"),
    ],
)
def test_format_website(website: str, formatted_website: str):
    assert formatted_website == format_website(website)

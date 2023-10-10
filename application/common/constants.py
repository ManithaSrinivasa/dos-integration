PHARMACY_ORG_TYPE_ID = "PHA"

CLOSED_AND_HIDDEN_STATUSES = ["HIDDEN", "CLOSED"]

PHARMACY_SERVICE_TYPE_IDS = [13, 131, 132, 134, 137, 148, 149]
PHARMACY_ORGANISATION_SUB_TYPES = ["Community"]
PHARMACY_ODSCODE_LENGTH = 5
PHARMACY_SERVICE_TYPE_ID = 13

DOS_DEMOGRAPHICS_AREA_TYPE = "demographic"
DOS_CLINICAL_AREA_TYPE = "clinical"

DOS_POSTCODE_CHANGE_KEY = "postalcode"
DOS_WEBSITE_CHANGE_KEY = "cmsurl"
DOS_ADDRESS_CHANGE_KEY = "postaladdress"
DOS_PUBLIC_PHONE_CHANGE_KEY = "cmstelephoneno"
DOS_EASTING_CHANGE_KEY = "cmseastings"
DOS_NORTHING_CHANGE_KEY = "cmsnorthings"
DOS_POSTAL_TOWN_CHANGE_KEY = "cmsorgtown"
DI_LATITUDE_CHANGE_KEY = "latitude"  # DoS doesn't have a latitude change key so using one made up
DI_LONGITUDE_CHANGE_KEY = "longitude"  # DoS doesn't have a longitude change key so using one made up
DOS_SPECIFIED_OPENING_TIMES_CHANGE_KEY = "cmsopentimespecified"
DOS_STANDARD_OPENING_TIMES_MONDAY_CHANGE_KEY = "cmsopentimemonday"
DOS_STANDARD_OPENING_TIMES_TUESDAY_CHANGE_KEY = "cmsopentimetuesday"
DOS_STANDARD_OPENING_TIMES_WEDNESDAY_CHANGE_KEY = "cmsopentimewednesday"
DOS_STANDARD_OPENING_TIMES_THURSDAY_CHANGE_KEY = "cmsopentimethursday"
DOS_STANDARD_OPENING_TIMES_FRIDAY_CHANGE_KEY = "cmsopentimefriday"
DOS_STANDARD_OPENING_TIMES_SATURDAY_CHANGE_KEY = "cmsopentimesaturday"
DOS_STANDARD_OPENING_TIMES_SUNDAY_CHANGE_KEY = "cmsopentimesunday"
DOS_SGSDID_CHANGE_KEY = "cmssgsdid"
DOS_STATUS_CHANGE_KEY = "cmsorgstatus"

DOS_SERVICES_TABLE_CHANGE_TYPE_LIST = [
    DOS_ADDRESS_CHANGE_KEY,
    DOS_EASTING_CHANGE_KEY,
    DOS_NORTHING_CHANGE_KEY,
    DOS_POSTAL_TOWN_CHANGE_KEY,
    DOS_POSTCODE_CHANGE_KEY,
    DOS_PUBLIC_PHONE_CHANGE_KEY,
    DOS_WEBSITE_CHANGE_KEY,
    DOS_STATUS_CHANGE_KEY,
]
DI_CHANGE_KEYS_LIST = [DI_LATITUDE_CHANGE_KEY, DI_LONGITUDE_CHANGE_KEY]

DOS_STANDARD_OPENING_TIMES_CHANGE_KEY_LIST = [
    DOS_STANDARD_OPENING_TIMES_MONDAY_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_TUESDAY_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_WEDNESDAY_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_THURSDAY_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_FRIDAY_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_SATURDAY_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_SUNDAY_CHANGE_KEY,
]

DI_CHANGE_ITEMS = [
    DOS_ADDRESS_CHANGE_KEY,
    DOS_EASTING_CHANGE_KEY,
    DOS_NORTHING_CHANGE_KEY,
    DOS_POSTAL_TOWN_CHANGE_KEY,
    DOS_POSTCODE_CHANGE_KEY,
    DOS_PUBLIC_PHONE_CHANGE_KEY,
    DOS_WEBSITE_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_MONDAY_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_TUESDAY_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_WEDNESDAY_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_THURSDAY_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_FRIDAY_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_SATURDAY_CHANGE_KEY,
    DOS_STANDARD_OPENING_TIMES_SUNDAY_CHANGE_KEY,
]
DOS_INTEGRATION_USER_NAME = "DOS_INTEGRATION"

DOS_SERVICE_HISTORY_ACTIVE_STATUS = "active"
DOS_SERVICE_HISTORY_CLOSED_STATUS = "closed"

# Service Statuses
DOS_ACTIVE_STATUS_ID = 1
DOS_CLOSED_STATUS_ID = 2
DOS_COMMISSIONING_STATUS_ID = 3

# Palliative Care
MAIN_PHARMACY_ODSCODE_LENGTH = 5
DOS_PALLIATIVE_CARE_TYPE_ID = 13
NHS_UK_PALLIATIVE_CARE_SERVICE_CODE = "SRV0559"
DOS_PALLIATIVE_CARE_SYMPTOM_GROUP = 360
DOS_PALLIATIVE_CARE_SYMPTOM_DISCRIMINATOR = 14167
DOS_PHARMACY_NO_PALLIATIVE_CARE_TYPES = [131, 132, 134, 137, 148, 149]
DOS_PALLIATIVE_CARE_SGSDID = f"{DOS_PALLIATIVE_CARE_SYMPTOM_GROUP}={DOS_PALLIATIVE_CARE_SYMPTOM_DISCRIMINATOR}"

# Blood Pressure
DOS_BLOOD_PRESSURE_TYPE_ID = 148
NHS_UK_BLOOD_PRESSURE_SERVICE_CODE = "SRV0560"
DOS_BLOOD_PRESSURE_SYMPTOM_GROUP = 360
DOS_BLOOD_PRESSURE_SYMPTOM_DISCRIMINATOR = 14207
DOS_BLOOD_PRESSURE_SGSDID = f"{DOS_BLOOD_PRESSURE_SYMPTOM_GROUP}={DOS_BLOOD_PRESSURE_SYMPTOM_DISCRIMINATOR}"

# Contraception
DOS_CONTRACEPTION_TYPE_ID = 149
NHS_UK_CONTRACEPTION_SERVICE_CODE = "SRV2000"
DOS_CONTRACEPTION_SYMPTOM_GROUP = 360
DOS_CONTRACEPTION_SYMPTOM_DISCRIMINATOR = 14210
DOS_CONTRACEPTION_SGSDID = f"{DOS_CONTRACEPTION_SYMPTOM_GROUP}={DOS_CONTRACEPTION_SYMPTOM_DISCRIMINATOR}"

HIDDEN_OR_CLOSED_REPORT_ID = "HIDDEN_OR_CLOSED"
UNMATCHED_PHARMACY_REPORT_ID = "UNMATCHED_PHARMACY"
INVALID_POSTCODE_REPORT_ID = "INVALID_POSTCODE"
INVALID_OPEN_TIMES_REPORT_ID = "INVALID_OPEN_TIMES"
DLQ_HANDLER_REPORT_ID = "CR_DLQ_HANDLER_RECEIVED_EVENT"
FIFO_DLQ_HANDLER_REPORT_ID = "FIFO_DLQ_HANDLER_RECEIVED_EVENT"
UNMATCHED_SERVICE_TYPE_REPORT_ID = "UNMATCHED_SERVICE_TYPE"
GENERIC_BANK_HOLIDAY_REPORT_ID = "GENERIC_BANK_HOLIDAY"
GENERIC_CHANGE_EVENT_ERROR_REPORT_ID = "GENERIC_CHANGE_EVENT_ERROR"

METRIC_REPORT_KEY_MAP = {
    "InvalidPostcode": INVALID_POSTCODE_REPORT_ID,
    "InvalidOpenTimes": INVALID_OPEN_TIMES_REPORT_ID,
}

PHARMACY_SERVICE_KEY = "PHARMACY"
DENTIST_SERVICE_KEY = "DENTIST"
PHARMACY_ORG_TYPE_ID = "PHA"
DENTIST_ORG_TYPE_ID = "Dentist"
SERVICE_TYPES_ALIAS_KEY = "SERVICE_TYPE_NAME"
ORGANISATION_SUB_TYPES_KEY = "ORGANISATION_SUB_TYPES"
VALID_SERVICE_TYPES_KEY = "VALID_SERVICE_TYPES"
ODSCODE_LENGTH_KEY = "ODSCODE_LENGTH"

SERVICE_TYPES = {
    PHARMACY_ORG_TYPE_ID: {
        SERVICE_TYPES_ALIAS_KEY: PHARMACY_SERVICE_KEY,
        ORGANISATION_SUB_TYPES_KEY: ["Community"],
        VALID_SERVICE_TYPES_KEY: [13, 131, 132, 134, 137],
        ODSCODE_LENGTH_KEY: 5,
    },
    DENTIST_ORG_TYPE_ID: {
        SERVICE_TYPES_ALIAS_KEY: DENTIST_SERVICE_KEY,
        ORGANISATION_SUB_TYPES_KEY: ["TBA"],
        VALID_SERVICE_TYPES_KEY: [12],
        ODSCODE_LENGTH_KEY: 7,
    },
}

DENTIST_SERVICE_TYPE_IDS = SERVICE_TYPES[DENTIST_ORG_TYPE_ID][VALID_SERVICE_TYPES_KEY]
PHARMACY_SERVICE_TYPE_IDS = SERVICE_TYPES[PHARMACY_ORG_TYPE_ID][VALID_SERVICE_TYPES_KEY]

from json import loads
from typing import Any, Dict, Union
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord


logger = Logger()


def extract_body(body: str) -> Dict[str, Any]:
    """Extracts the event body from the lambda function invocation event

    Args:
        message_body (str): A JSON string body
    Returns:
        Dict[str, Any]: Message body as a dictionary
    """
    try:
        body = loads(body)
    except Exception:
        logger.exception("Change Event unable to be extracted")
        raise
    return body


def get_sequence_number(record: SQSRecord) -> Union[int, None]:
    """Gets the sequence number from the SQS record
    Args:
        record (SQSRecord): SQS record
    Returns:
        Optional[int]: Sequence number of the message or None if not present
    """
    seq_num_str = record.message_attributes.get("sequence-number", {}).get("stringValue")
    return None if seq_num_str is None else int(seq_num_str)


def get_sqs_msg_attribute(msg_attributes: Dict[str, Any], key: str) -> Union[str, float, None]:
    attribute = msg_attributes.get(key)
    if attribute is None:
        return None
    data_type = attribute.get("dataType")
    if data_type == "String":
        return attribute.get("stringValue")
    if data_type == "Number":
        return float(attribute.get("stringValue"))


def handle_sqs_msg_attributes(msg_attributes: Dict[str, Any]) -> Dict[str, Any]:
    attributes = {"error_msg": "", "error_msg_http_code": ""}
    if msg_attributes is not None:
        if "error_msg_http_code" in msg_attributes:
            attributes["error_msg_http_code"] = msg_attributes["error_msg_http_code"]["stringValue"]
        if "error_msg" in msg_attributes:
            attributes["error_msg"] = msg_attributes["error_msg"]["stringValue"]

        return attributes

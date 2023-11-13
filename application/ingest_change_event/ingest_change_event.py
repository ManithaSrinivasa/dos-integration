from json import dumps
from os import environ
from time import gmtime, strftime
from typing import Any

from aws_embedded_metrics import metric_scope
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.utilities.data_classes import SQSEvent, event_source
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from boto3 import client

from .change_event_validation import validate_change_event
from common.dynamodb import add_change_event_to_dynamodb, get_latest_sequence_id_for_a_given_odscode_from_dynamodb
from common.middlewares import redact_staff_key_from_event, unhandled_exception_logging
from common.types import HoldingQueueChangeEventItem
from common.utilities import extract_body, get_sequence_number

logger = Logger()
tracer = Tracer()
sqs = client("sqs")


@redact_staff_key_from_event()
@unhandled_exception_logging()
@tracer.capture_lambda_handler()
@event_source(data_class=SQSEvent)
@logger.inject_lambda_context(
    clear_state=True,
    correlation_id_path='Records[0].messageAttributes."correlation-id".stringValue',
)
@metric_scope
def lambda_handler(event: SQSEvent, context: LambdaContext, metrics: Any) -> None:  # noqa: ANN401, ARG001
    """Entrypoint handler for the ingest change event lambda.

    This lambda runs the change event validation, puts the change event on the dynamodb table
    and then sends the validated change event to the delay queue.

    Args:
        event (SQSEvent): Lambda function invocation event
        context (LambdaContext): Lambda function context object
        metrics (Any): Embedded metrics object

    Event: The event payload should contain an Update Request
    """
    if len(list(event.records)) != 1:
        msg = f"{len(list(event.records))} records found in event. Expected 1."
        raise ValueError(msg)

    record = next(event.records)
    change_event = extract_body(record.body)
    validate_change_event(change_event)
    ods_code = change_event.get("ODSCode")
    add_change_event_received_metric(ods_code=ods_code)
    logger.append_keys(ods_code=ods_code)
    sequence_number = get_sequence_number(record)
    sqs_timestamp = int(record.attributes["SentTimestamp"])
    s, ms = divmod(sqs_timestamp, 1000)
    logger.info(
        "Change Event received",
        sequence_number=sequence_number,
        message_received="%s.%03d" % (strftime("%Y-%m-%d %H:%M:%S", gmtime(s)), ms),
    )
    logger.debug("Getting latest sequence number")
    db_latest_sequence_number = get_latest_sequence_id_for_a_given_odscode_from_dynamodb(ods_code)
    logger.info("Writing change event to dynamo")
    record_id = add_change_event_to_dynamodb(change_event, sequence_number, sqs_timestamp)
    logger.append_keys(dynamo_record_id=record_id)

    if sequence_number is None:
        logger.error("No sequence number provided, so message will be ignored.")
        return
    elif sequence_number < db_latest_sequence_number:  # noqa: RET505
        logger.error(
            "Sequence id is smaller than the existing one in db for a given odscode, so will be ignored",
            incoming_sequence_number=sequence_number,
            db_latest_sequence_number=db_latest_sequence_number,
        )
        return
    holding_queue_change_event_item = HoldingQueueChangeEventItem(
        change_event=change_event,
        sequence_number=sequence_number,
        message_received=sqs_timestamp,
        dynamo_record_id=record_id,
        correlation_id=logger.get_correlation_id(),
    )
    logger.debug("Change event validated", holding_queue_change_event_item=holding_queue_change_event_item)
    sqs.send_message(
        QueueUrl=environ["HOLDING_QUEUE_URL"],
        MessageBody=dumps(holding_queue_change_event_item),
        MessageGroupId=ods_code,
    )


@metric_scope
def add_change_event_received_metric(ods_code: str, metrics: Any) -> None:  # noqa: ANN401
    """Adds a success metric to the custom metrics collection.

    Args:
        ods_code (str): ODS Code of the change event
        metrics (Any): Embedded metrics object
    """
    metrics.set_namespace("UEC-DOS-INT")
    metrics.set_property("message", f"Change Event Received for ODSCode: {ods_code}")
    metrics.set_property("ods_code", ods_code)
    metrics.set_dimensions({"ENV": environ["ENV"]})
    metrics.set_property("level", "WARNING")
    metrics.put_metric("ChangeEventReceived", 1, "Count")

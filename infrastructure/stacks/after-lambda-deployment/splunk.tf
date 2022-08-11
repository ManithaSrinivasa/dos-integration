resource "aws_cloudwatch_log_subscription_filter" "service_matcher_logs_subscription_filter" {
  name            = var.service_matcher_subscription_filter_name
  role_arn        = data.aws_iam_role.firehose_role.arn
  log_group_name  = "/aws/lambda/${var.service_matcher_lambda_name}"
  filter_pattern  = ""
  destination_arn = data.aws_kinesis_firehose_delivery_stream.dos_integration_firehose.arn
  depends_on      = [time_sleep.wait_a_minute]
}

resource "aws_cloudwatch_log_subscription_filter" "service_sync_logs_subscription_filter" {
  name            = var.service_sync_subscription_filter_name
  role_arn        = data.aws_iam_role.firehose_role.arn
  log_group_name  = "/aws/lambda/${var.service_sync_lambda_name}"
  filter_pattern  = ""
  destination_arn = data.aws_kinesis_firehose_delivery_stream.dos_integration_firehose.arn
  depends_on      = [time_sleep.wait_a_minute]
}

resource "aws_cloudwatch_log_subscription_filter" "orchestrator_logs_subscription_filter" {
  name            = var.orchestrator_subscription_filter_name
  role_arn        = data.aws_iam_role.firehose_role.arn
  log_group_name  = "/aws/lambda/${var.orchestrator_lambda_name}"
  filter_pattern  = ""
  destination_arn = data.aws_kinesis_firehose_delivery_stream.dos_integration_firehose.arn
  depends_on      = [time_sleep.wait_a_minute]
}

resource "aws_cloudwatch_log_subscription_filter" "change_event_dlq_handler_logs_subscription_filter" {
  name            = var.change_event_dlq_handler_subscription_filter_name
  role_arn        = data.aws_iam_role.firehose_role.arn
  log_group_name  = "/aws/lambda/${var.change_event_dlq_handler_lambda_name}"
  filter_pattern  = ""
  destination_arn = data.aws_kinesis_firehose_delivery_stream.dos_integration_firehose.arn
  depends_on      = [time_sleep.wait_a_minute]
}

resource "aws_cloudwatch_log_subscription_filter" "dos_db_update_dlq_handler_logs_subscription_filter" {
  name            = var.dos_db_update_dlq_handler_subscription_filter_name
  role_arn        = data.aws_iam_role.firehose_role.arn
  log_group_name  = "/aws/lambda/${var.dos_db_update_dlq_handler_lambda_name}"
  filter_pattern  = ""
  destination_arn = data.aws_kinesis_firehose_delivery_stream.dos_integration_firehose.arn
  depends_on      = [time_sleep.wait_a_minute]
}

resource "aws_cloudwatch_log_subscription_filter" "event_replay_logs_subscription_filter" {
  name            = var.event_replay_subscription_filter_name
  role_arn        = data.aws_iam_role.firehose_role.arn
  log_group_name  = "/aws/lambda/${var.event_replay_lambda_name}"
  filter_pattern  = ""
  destination_arn = data.aws_kinesis_firehose_delivery_stream.dos_integration_firehose.arn
  depends_on      = [time_sleep.wait_a_minute]
}

resource "aws_cloudwatch_log_subscription_filter" "di_endpoint_access_logs" {
  name            = var.change_event_gateway_subscription_filter_name
  role_arn        = data.aws_iam_role.firehose_role.arn
  log_group_name  = "/aws/api-gateway/${var.di_endpoint_api_gateway_name}"
  filter_pattern  = ""
  destination_arn = data.aws_kinesis_firehose_delivery_stream.dos_integration_firehose.arn
  depends_on      = [time_sleep.wait_a_minute]
}

resource "time_sleep" "wait_a_minute" {
  create_duration = "1m"
}

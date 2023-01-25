resource "aws_cloudwatch_metric_alarm" "change_event_dlq_handler_error_rate_alert" {
  alarm_actions             = [data.aws_sns_topic.sns_topic_app_alerts_for_slack_default_region.arn]
  alarm_description         = "Change Event DLQ Handler error rate has exceeded 10%"
  alarm_name                = "${var.project_id} | ${var.blue_green_environment} | Change Event DLQ Handler Error Rate"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  threshold                 = "10"
  insufficient_data_actions = []

  metric_query {
    id          = "expression"
    expression  = "(errors/invocations) * 100"
    label       = "Error Rate (%)"
    return_data = "true"
  }

  metric_query {
    id = "errors"
    metric {
      metric_name = "Errors"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.change_event_dlq_handler_lambda_name
      }
    }
  }

  metric_query {
    id = "invocations"
    metric {
      metric_name = "Invocations"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.change_event_dlq_handler_lambda_name
      }
    }
  }
}

resource "aws_cloudwatch_metric_alarm" "dos_db_update_dlq_handler_error_rate_alert" {
  alarm_actions             = [data.aws_sns_topic.sns_topic_app_alerts_for_slack_default_region.arn]
  alarm_description         = "DoS DB Update DLQ Handler error rate has exceeded 10%"
  alarm_name                = "${var.project_id} | ${var.blue_green_environment} | DoS DB Update DLQ Handler Error Rate"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  threshold                 = "10"
  insufficient_data_actions = []

  metric_query {
    id          = "expression"
    expression  = "(errors/invocations) * 100"
    label       = "Error Rate (%)"
    return_data = "true"
  }

  metric_query {
    id = "errors"
    metric {
      metric_name = "Errors"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.dos_db_update_dlq_handler_lambda_name
      }
    }
  }

  metric_query {
    id = "invocations"
    metric {
      metric_name = "Invocations"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.dos_db_update_dlq_handler_lambda_name
      }
    }
  }
}

resource "aws_cloudwatch_metric_alarm" "event_replay_error_rate_alert" {
  alarm_actions             = [data.aws_sns_topic.sns_topic_app_alerts_for_slack_default_region.arn]
  alarm_description         = "Event Replay error rate has exceeded 10%"
  alarm_name                = "${var.project_id} | ${var.blue_green_environment} | Event Replay Error Rate"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  threshold                 = "10"
  insufficient_data_actions = []

  metric_query {
    id          = "expression"
    expression  = "(errors/invocations) * 100"
    label       = "Error Rate (%)"
    return_data = "true"
  }

  metric_query {
    id = "errors"
    metric {
      metric_name = "Errors"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.event_replay_lambda_name
      }
    }
  }

  metric_query {
    id = "invocations"
    metric {
      metric_name = "Invocations"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.event_replay_lambda_name
      }
    }
  }
}

resource "aws_cloudwatch_metric_alarm" "ingest_change_event_error_rate_alert" {
  alarm_actions             = [data.aws_sns_topic.sns_topic_app_alerts_for_slack_default_region.arn]
  alarm_description         = "Ingest Change Event error rate has exceeded 10%"
  alarm_name                = "${var.project_id} | ${var.blue_green_environment} | Ingest Change Event Error Rate"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  threshold                 = "10"
  insufficient_data_actions = []

  metric_query {
    id          = "expression"
    expression  = "(errors/invocations) * 100"
    label       = "Error Rate (%)"
    return_data = "true"
  }

  metric_query {
    id = "errors"
    metric {
      metric_name = "Errors"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.ingest_change_event_lambda_name
      }
    }
  }

  metric_query {
    id = "invocations"
    metric {
      metric_name = "Invocations"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.ingest_change_event_lambda_name
      }
    }
  }
}

resource "aws_cloudwatch_metric_alarm" "orchestrator_error_rate_alert" {
  alarm_actions             = [data.aws_sns_topic.sns_topic_app_alerts_for_slack_default_region.arn]
  alarm_description         = "Orchestrator error rate has exceeded 10%"
  alarm_name                = "${var.project_id} | ${var.blue_green_environment} | Orchestrator Error Rate"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  threshold                 = "10"
  insufficient_data_actions = []

  metric_query {
    id          = "expression"
    expression  = "(errors/invocations) * 100"
    label       = "Error Rate (%)"
    return_data = "true"
  }

  metric_query {
    id = "errors"
    metric {
      metric_name = "Errors"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.orchestrator_lambda_name
      }
    }
  }

  metric_query {
    id = "invocations"
    metric {
      metric_name = "Invocations"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.orchestrator_lambda_name
      }
    }
  }
}

resource "aws_cloudwatch_metric_alarm" "send_email_error_rate_alert" {
  alarm_actions             = [data.aws_sns_topic.sns_topic_app_alerts_for_slack_default_region.arn]
  alarm_description         = "Send Email error rate has exceeded 10%"
  alarm_name                = "${var.project_id} | ${var.blue_green_environment} | Send Email Error Rate"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  threshold                 = "10"
  insufficient_data_actions = []

  metric_query {
    id          = "expression"
    expression  = "(errors/invocations) * 100"
    label       = "Error Rate (%)"
    return_data = "true"
  }

  metric_query {
    id = "errors"
    metric {
      metric_name = "Errors"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.send_email_lambda_name
      }
    }
  }

  metric_query {
    id = "invocations"
    metric {
      metric_name = "Invocations"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.send_email_lambda_name
      }
    }
  }
}

resource "aws_cloudwatch_metric_alarm" "service_matcher_error_rate_alert" {
  alarm_actions             = [data.aws_sns_topic.sns_topic_app_alerts_for_slack_default_region.arn]
  alarm_description         = "Service Matcher error rate has exceeded 10%"
  alarm_name                = "${var.project_id} | ${var.blue_green_environment} | Service Matcher Error Rate"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  threshold                 = "10"
  insufficient_data_actions = []

  metric_query {
    id          = "expression"
    expression  = "(errors/invocations) * 100"
    label       = "Error Rate (%)"
    return_data = "true"
  }

  metric_query {
    id = "errors"
    metric {
      metric_name = "Errors"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.service_matcher_lambda_name
      }
    }
  }

  metric_query {
    id = "invocations"
    metric {
      metric_name = "Invocations"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.service_matcher_lambda_name
      }
    }
  }
}

resource "aws_cloudwatch_metric_alarm" "service_sync_error_rate_alert" {
  alarm_actions             = [data.aws_sns_topic.sns_topic_app_alerts_for_slack_default_region.arn]
  alarm_description         = "Service Sync error rate has exceeded 10%"
  alarm_name                = "${var.project_id} | ${var.blue_green_environment} | Service Sync Error Rate"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  threshold                 = "10"
  insufficient_data_actions = []

  metric_query {
    id          = "expression"
    expression  = "(errors/invocations) * 100"
    label       = "Error Rate (%)"
    return_data = "true"
  }

  metric_query {
    id = "errors"
    metric {
      metric_name = "Errors"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.service_sync_lambda_name
      }
    }
  }

  metric_query {
    id = "invocations"
    metric {
      metric_name = "Invocations"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.service_sync_lambda_name
      }
    }
  }
}

resource "aws_cloudwatch_metric_alarm" "slack_messenger_error_rate_alert" {
  alarm_actions             = [data.aws_sns_topic.sns_topic_app_alerts_for_slack_default_region.arn]
  alarm_description         = "Slack Messenger error rate has exceeded 10%"
  alarm_name                = "${var.project_id} | ${var.blue_green_environment} | Slack Messenger Error Rate"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  threshold                 = "10"
  insufficient_data_actions = []

  metric_query {
    id          = "expression"
    expression  = "(errors/invocations) * 100"
    label       = "Error Rate (%)"
    return_data = "true"
  }

  metric_query {
    id = "errors"
    metric {
      metric_name = "Errors"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.slack_messenger_lambda_name
      }
    }
  }

  metric_query {
    id = "invocations"
    metric {
      metric_name = "Invocations"
      namespace   = "AWS/Lambda"
      period      = "120"
      stat        = "Sum"
      unit        = "Count"
      dimensions = {
        FunctionName = var.slack_messenger_lambda_name
      }
    }
  }
}

# ##############
# # LAMBDA
# ##############

variable "ingest_change_event_lambda_name" {
  type        = string
  description = "Name of ingest change event lambda"
}

variable "slack_messenger_lambda_name" {
  type        = string
  description = "Name of slack messenger lambda"
}

variable "change_event_dlq_handler_lambda_name" {
  type        = string
  description = "Name of change event dlq handler lambda"
}

# ##############
# # SQS
# ##############

variable "change_event_queue_name" {
  type        = string
  description = "Change event queue name"
}

variable "shared_resources_dlq" {
  type        = string
  description = "DLQ for change event queue"
}

# ##############
# # SNS
# ##############

variable "shared_resources_sns_topic_app_alerts_for_slack_default_region" {
  type        = string
  description = "The name of the sns topic to recieve alerts for the application to forward to slack in the default region (shared resources)"
}

variable "shared_resources_sns_topic_app_alerts_for_slack_route53_health_check_alarm_region" {
  type        = string
  description = "The name of the sns topic to recieve alerts for the application to forward to slack in the route53 health check alarm region (shared resources)"
}

# ##############
# # CONDITIONS
# ##############

variable "attach_to_environment" {
  default     = true
  type        = bool
  description = "Whether to attach this stack to the environment, if true then the stack will be attached to the environment else some will be removed"

}

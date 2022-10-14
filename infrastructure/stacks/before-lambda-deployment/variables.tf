############
# VPC
############

variable "vpc_terraform_state_key" {
  description = "Texas Platform State store bucket key"
}

# ############################
# # SECRETS
# ############################

variable "api_gateway_api_key_name" {
  description = "API Key for DI AWS API Gateway"
}

variable "nhs_uk_api_key_key" {
  description = "API Key key for secrets manager"
}



# ############################
# # SECURITY GROUP / RULES
# ############################

variable "lambda_security_group_name" {
  description = "Name of the lambda security group"
}

variable "dos_db_name" {
  description = "Name of db dos instance to connect to"
}

variable "dos_db_replica_name" {
  description = "Name of db dos read replica instance to connect to"
}

# ############################
# # IAM
# ############################
variable "orchestrator_role_name" {
  description = "Role name for event processor lambda"
}

variable "change_event_dlq_handler_role_name" {
  description = "Role name for change event dlq handler lambda"
}

variable "dos_db_update_dlq_handler_role_name" {
  description = "Role name for dos db update dlq handler lambda"
}

variable "slack_messenger_role_name" {
  description = "Role name for slack messenger dlq handler lambda"
}

variable "event_replay_role_name" {
  description = "Role name for event replay lambda"
}

variable "dos_db_handler_role_name" {
  description = "Role name for dos db handler lambda"
}
variable "send_email_role_name" {
  description = "Role name for send email lambda"
}


# ##############
# # LAMBDAS
# ##############

variable "service_matcher_lambda_name" {
  type        = string
  description = "Name of service matcher lambda"
}

variable "service_sync_lambda_name" {
  type        = string
  description = "Name of service sync lambda"
}

variable "change_event_dlq_handler_lambda_name" {
  type        = string
  description = "Name of change event dlq handler lambda"
}

variable "dos_db_update_dlq_handler_lambda_name" {
  type        = string
  description = "Name of dos db update dlq handler lambda"
}

variable "dos_db_handler_lambda_name" {
  type        = string
  description = "Name of dos db handler lambda"
}

variable "send_email_lambda_name" {
  type        = string
  description = "Name of send email lambda"
}
# ############################
# Old Variables - remove after release 3.0
# ############################

variable "event_processor_role_name" {
  description = "Role name for event processor lambda"
}

variable "event_sender_role_name" {
  description = "Role name for event sender lambda"
}

variable "fifo_dlq_handler_role_name" {
  description = "Role name for fifo dlq handler lambda"
}

variable "cr_fifo_dlq_handler_role_name" {
  description = "Role name for cr_fifo dlq handler lambda"
}

variable "fifo_queue_name" {
  description = ""
}
variable "cr_fifo_queue_name" {
  description = ""
}

variable "dead_letter_queue_from_fifo_queue_name" {
  description = ""
}

variable "cr_dead_letter_queue_from_fifo_queue_name" {
  description = ""
}
# ##############
# # DYNAMO DB
# ##############

variable "change_events_table_name" {
  description = "Name of the table that stores received pharmacy change events"
}

############
# SQS
############

variable "change_event_queue_name" {
  description = ""
}

variable "update_request_queue_name" {
  description = ""
}

variable "change_event_dlq" {
  description = ""
}

variable "update_request_dlq" {
  description = ""
}

# ##############
# # KMS
# ##############

variable "signing_key_alias" {
  description = "Alias of key used for signing in the default region"
}

variable "alarm_region_signing_key_alias" {
  description = "Alias of key used for signing in the alarm region"
}

variable "developer_role_name" {
  description = "Role name of developer's role so that it can access the KMS key for the dbcloner"
}

# ######################
# # CLOUDWATCH ALERTS
# #######################

variable "sns_topic_app_alerts_for_slack_default_region" {
  description = "The name of the sns topic to recieve alerts for the application to forward to slack in the default region"
}

variable "sns_topic_app_alerts_for_slack_alarm_region" {
  description = "The name of the sns topic to recieve alerts for the application to forward to slack in the alarm region"
}

# ##############
# # S3
# ##############

variable "send_email_bucket_name" {
  type        = string
  description = "Name of the bucket to temporarily store emails to be sent"
}

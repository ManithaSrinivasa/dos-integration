resource "aws_ssm_parameter" "blue_green_deployment_previous_version" {
  #checkov:skip=CKV2_AWS_34:Value does not contain sensitive data so it is ok to be stored in plain text
  name        = var.blue_green_deployment_previous_version_parameter_name
  description = "The name of the blue/green environment that is connected to the shared resources. DO NOT CHANGE THIS VALUE MANUALLY IT WILL NOT EFFECT DEPLOYMENTS."
  type        = "String"
  value       = var.previous_blue_green_environment
}

resource "aws_ssm_parameter" "blue_green_deployment_current_version" {
  #checkov:skip=CKV2_AWS_34:Value does not contain sensitive data so it is ok to be stored in plain text
  name        = var.blue_green_deployment_current_version_parameter_name
  description = "The name of the blue/green environment that is connected to the shared resources. DO NOT CHANGE THIS VALUE MANUALLY IT WILL NOT EFFECT DEPLOYMENTS."
  type        = "String"
  value       = var.blue_green_environment
}

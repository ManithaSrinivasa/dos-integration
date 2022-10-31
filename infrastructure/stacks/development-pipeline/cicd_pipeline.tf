module "cicd_pipeline_artefact_bucket" {
  source             = "../../modules/s3"
  name               = "${var.project_id}-${var.environment}-cicd-pipeline-artefact-bucket-mgmt"
  project_id         = var.project_id
  acl                = "private"
  versioning_enabled = "true"
  force_destroy      = "true"
}

data "template_file" "unit_tests_buildspec" {
  template = file("unit-tests-buildspec.yml")
}

data "template_file" "build_buildspec" {
  template = file("build-buildspec.yml")
}

data "template_file" "build_image_buildspec" {
  template = file("build-image-buildspec.yml")
}

data "template_file" "deploy_buildspec" {
  template = file("deploy-buildspec.yml")
}

data "template_file" "integration_tests_buildspec" {
  template = file("integration-tests-buildspec.yml")
}

data "template_file" "delete_task_environment_from_tag_buildspec" {
  template = file("delete-task-environment-from-tag-buildspec.yml")
}

data "template_file" "delete_task_environment_on_pr_merged_buildspec" {
  template = file("delete-task-environment-on-pr-merged-buildspec.yml")
}

data "template_file" "build_environment_buildspec" {
  template = file("build-environment-buildspec.yml")
}

data "template_file" "delete_ecr_images_buildspec" {
  template = file("delete-ecr-images-buildspec.yml")
}

data "template_file" "build_release_buildspec" {
  template = file("build-release-buildspec.yml")
}

data "template_file" "delete_release_environment_and_pipeline_on_pr_merged_buildspec" {
  template = file("delete-release-environment-and-pipeline-on-pr-merged-buildspec.yml")
}

data "template_file" "demo_deploy_buildspec" {
  template = file("demo-deploy-buildspec.yml")
}

data "aws_iam_role" "pipeline_role" {
  name = "UECPUPipelineRole"
}

locals {
  deploy_envs      = toset(["dev", "test", "perf"])
  to_build         = toset(["event-sender", "event-processor", "fifo-dlq-handler", "orchestrator", "cr-fifo-dlq-handler", "test-db-checker-handler", "event-replay", "authoriser", "dos-api-gateway", "slack-messenger"])
  integration_tags = toset(["pharmacy_cloudwatch_queries", "pharmacy_no_log_searches"])
  independent_build_images = {
    tester = {
      "filematch" = "requirement"
    }
    serverless = {
      "filematch" = "serverless.yml"
    }
  }
}

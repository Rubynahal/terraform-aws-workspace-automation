# Get AWS account ID
data "aws_caller_identity" "current" {}

##########################
# Lambda Function
##########################

module "lambda_function" {
  source = "./modules/lambda"

  vpc_security_group_ids = var.vpc_security_group_ids
  vpc_subnet_ids         = var.vpc_subnet_ids

  function_name          = var.function_name
  description            = var.description
  handler                = var.handler
  runtime                = var.runtime

  store_on_s3            = var.store_on_s3
  s3_bucket              = var.store_on_s3 && var.s3_bucket == null ? aws_s3_bucket.this[0].id : var.s3_bucket
  local_existing_package = "${path.module}/ws-function/lambda_function.py.zip"
  kms_key_arn            = var.lambda_kms_key_arn

  cloudwatch_logs_retention_in_days = var.cloudwatch_logs_retention_in_days
  cloudwatch_logs_kms_key_id        = var.cloudwatch_kms_key_arn
  policy_kms_key_arns               = [var.workspaces_kms_key]
  timeout      = 600
  tracing_mode = var.tracing_mode

  environment_variables = {
    CAMPUS_DIR_ID            = var.campus_dir_id
    SDE_DIR_ID               = var.sde_dir_id
    SOM_DIR_ID               = var.som_dir_id
    UMC_DIR_ID               = var.umc_dir_id
    WIN_PERF_BUNDLE_ID       = var.win_perf_bundle_id
    WIN_GPU_BUNDLE_ID        = var.win_gpu_bundle_id
    LINUX_PERF_BUNDLE_ID     = var.linux_perf_bundle_id
    LINUX_POWERPRO_BUNDLE_ID = var.linux_powerpro_bundle_id
    WORKSPACE_KMS_KEY        = var.workspaces_kms_key
  }

  allowed_triggers = {
    S3Trigger = {
      service    = "s3"
      source_arn = "arn:aws:s3:::${var.source_bucket}"
      source_account = data.aws_caller_identity.current.id
    }
  }
  source_bucket = var.source_bucket

  cloudwatch_logs_tags = var.tags
  role_tags            = var.tags
  tags                 = var.tags
}

##########################
# S3 Bucket
##########################

resource "aws_s3_bucket" "this" {
  count = var.store_on_s3 && var.s3_bucket == null ? 1 : 0

  bucket = var.bucket_name
  acl    = var.acl

  tags = var.tags
}

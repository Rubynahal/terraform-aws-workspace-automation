variable "vpc_security_group_ids" {
  type = list(any)
}
variable "vpc_subnet_ids" {
  type = list(any)
}
variable "function_name" {}
variable "description" {}
variable "handler" {}
variable "runtime" {}
variable "store_on_s3" {
  default = false
}
variable "s3_bucket" {
  default = null
}
variable "lambda_kms_key_arn" {}
variable "cloudwatch_kms_key_arn" {}
variable "cloudwatch_logs_retention_in_days" {}
variable "tags" {
  type = map(any)
}
variable "tracing_mode" {
  default = null
}
variable "campus_dir_id" {}
variable "sde_dir_id" {}
variable "som_dir_id" {}
variable "umc_dir_id" {}
variable "win_perf_bundle_id" {}
variable "win_gpu_bundle_id" {}
variable "linux_perf_bundle_id" {}
variable "linux_powerpro_bundle_id" {}
variable "workspaces_kms_key" {}
variable "source_bucket" {}
variable "bucket_name" {
  default = null
}
variable "acl" {
  default = "private"
}

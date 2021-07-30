# Lambda Function
output "this_lambda_function_arn" {
  description = "The ARN of the Lambda Function"
  value       = module.lambda_function.this_lambda_function_arn
}
output "this_lambda_function_name" {
  description = "The name of the Lambda Function"
  value       = module.lambda_function.this_lambda_function_name
}

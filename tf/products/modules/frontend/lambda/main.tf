data "archive_file" "fof_frontend" {
  type = "zip"
  source_dir = "src/lambda/frontend/${var.source_dir}"
  output_path = "lambda_${var.function_name}.zip"
}

resource "aws_lambda_function" "fof_frontend" {
  filename = data.archive_file.fof_frontend.output_path
  function_name = var.function_name
  handler = "lambda_function.handler"
  role = var.role
  description = var.description
  layers = [
    var.layer_arn,
    var.external_module_layer_arn]
  memory_size = var.memory
  runtime = "python3.8"
  timeout = var.timeout
  reserved_concurrent_executions = var.reserved_concurrent_executions
  publish = true
  environment {
    variables = var.environment
  }
  source_code_hash = data.archive_file.fof_frontend.output_base64sha256
  tags = {
    fof = "lambda"
  }
}

// TODO terraformでalias publishはどうやる？
//しかもmaster release のみ
//resource "aws_lambda_alias" "prd" {
//  function_name    = aws_lambda_function.fof_states_lambda.function_name
//  function_version = aws_lambda_function.fof_states_lambda.version
//  name             = "prd"
//}

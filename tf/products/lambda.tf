provider "aws" {
  region = "ap-northeast-1"
}

module "fof_sdk" {
  env = var.env
  source = "./modules/lambda_layer/"
}

// TODO var.env 入れたい
data "aws_lambda_layer_version" "external_module_layer" {
  layer_name = "alexa-packages"
}

module "fof_alexa_frontend" {
  env = var.env
  source = "./modules/frontend/lambda"
  function_name = "fof_alexa_frontend"
  memory = 128
  description = ""
  environment = {
    "BACKEND_SFN_ARN" = var.backend_sfn_arn
    "BACKEND_SFN_ARN_PRD" = var.backend_sfn_arn_prd
  }
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

module "fof_state_launch" {
  env = var.env
  source = "./modules/lambda/"
  function_name = "fof_state_launch"
  memory = 128
  description = ""
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

module "fof_state_oracle" {
  env = var.env
  source = "./modules/lambda/"
  function_name = "fof_state_oracle"
  memory = 128
  description = ""
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

module "fof_state_changer" {
  env = var.env
  source = "./modules/lambda/"
  function_name = "fof_state_changer"
  memory = 128
  description = ""
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

module "fof_manual_handler" {
  env = var.env
  source = "./modules/lambda/"
  function_name = "fof_manual_handler"
  memory = 128
  description = ""
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

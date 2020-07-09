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

resource "aws_lambda_permission" "alexa_permission" {
  action = "lambda:InvokeFunction"
  function_name = module.fof_alexa_frontend.function_name
  principal = "alexa-appkit.amazon.com"
  event_source_token = var.event_source_token

  depends_on = [
    module.fof_alexa_frontend]
}

module "fof_alexa_frontend" {
  env = var.env
  source = "./modules/frontend/lambda"
  function_name = "fof_alexa_frontend"
  memory = 128
  description = ""
  environment = {
    "BACKEND_SFN_ARN_STG" = var.backend_sfn_arn_stg
    "BACKEND_SFN_ARN_PRD" = var.backend_sfn_arn_prd
  }
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

module "fof_text_translator" {
  env = var.env
  source = "./modules/lambda"
  function_name = "fof_text_translator"
  description = ""
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

module "fof_pre_import_attr" {
  env = var.env
  source = "./modules/lambda/"
  function_name = "fof_pre_import_attr"
  description = ""
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

module "fof_state_translator" {
  env = var.env
  source = "./modules/lambda/"
  function_name = "fof_state_translator"
  description = ""
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

module "fof_state_launch" {
  env = var.env
  source = "./modules/lambda_with_env/"
  function_name = "fof_state_launch"
  memory = 128
  description = ""
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
  environment = {
    "ASSETS_URL_PREFIX" = var.assets_url_prefix
  }
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
  source = "./modules/lambda_with_env/"
  function_name = "fof_manual_handler"
  memory = 128
  description = ""
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
  environment = {
    "ASSETS_URL_PREFIX" = var.assets_url_prefix
  }
}

module "fof_state_tutorial" {
  env = var.env
  source = "./modules/lambda/"
  function_name = "fof_state_tutorial"
  memory = 128
  description = ""
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

module "fof_state_ganesha_shop" {
  env = var.env
  source = "./modules/lambda/"
  function_name = "fof_state_ganesha_shop"
  memory = 128
  description = ""
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

module "fof_post_save_attr" {
  env = var.env
  source = "./modules/lambda/"
  function_name = "fof_post_save_attr"
  memory = 128
  description = ""
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

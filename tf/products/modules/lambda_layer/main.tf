data "archive_file" "fof_sdk" {
  type = "zip"
  source_dir = "src/lambda_layer/"
  output_path = "fof_sdk.zip"
}

resource "aws_lambda_layer_version" "fof_sdk" {
  filename = data.archive_file.fof_sdk.output_path
  layer_name = "fof_sdk_${var.env}"
  compatible_runtimes = [
    "python3.7",
    "python3.8"]
  source_code_hash = data.archive_file.fof_sdk.output_base64sha256
}

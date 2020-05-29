variable "env" {}
variable "function_name" {}
variable "description" {}
variable "layer_arn" {}
variable "external_module_layer_arn" {}
variable "memory" {
  default = 128
}
variable "timeout" {
  default = 3
}
variable "reserved_concurrent_executions" {
  default = -1
}
variable "role" {}

resource "aws_sfn_state_machine" "fof_backend_core" {
  name = "fof_backend_core_${var.env}"
  role_arn = var.sfn_role
  definition = templatefile("stepfunctions/fof_backend_core.json", {
    fof_manual_handler_arn = module.fof_manual_handler.arn
    fof_state_launch_arn = module.fof_state_launch.arn
    fof_state_oracle_arn = module.fof_state_oracle.arn
    fof_state_changer_arn = module.fof_state_changer.arn
  })
}

resource "aws_sfn_state_machine" "fof_backend_core" {
  name = "fof_backend_core_${var.env}"
  role_arn = var.sfn_role
  definition = templatefile("stepfunctions/fof_backend_core.asl", {
    fof_pre_import_attr_arn = module.fof_pre_import_attr.arn
    fof_state_translator_arn = module.fof_state_translator.arn
    fof_manual_handler_arn = module.fof_manual_handler.arn
    fof_intent_use_arn = module.fof_intent_use.arn
    fof_state_launch_arn = module.fof_state_launch.arn
    fof_state_oracle_arn = module.fof_state_oracle.arn
    fof_state_changer_arn = module.fof_state_changer.arn
    fof_state_tutorial_arn = module.fof_state_tutorial.arn
    fof_text_translator_arn = module.fof_text_translator.arn
    fof_state_ganesha_shop_arn = module.fof_state_ganesha_shop.arn
    fof_post_node_cleaner_arn = module.fof_post_node_cleaner.arn
    fof_post_save_attr_arn = module.fof_post_save_attr.arn
  })
}

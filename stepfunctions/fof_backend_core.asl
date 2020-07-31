{
  "Comment": "A Hello World example demonstrating various state types of the Amazon States Language",
  "StartAt": "ImportAttr",
  "States": {
    "ImportAttr": {
      "Comment": "DynamoDBからalexa_user_idをkeyとしてAttributesを取得する。",
      "Type": "Task",
      "Resource": "${fof_pre_import_attr_arn}",
      "ResultPath": "$.dynamo_attr",
      "Next": "StateTranslator"
    },
    "StateTranslator": {
      "Comment": "新規ユーザーはTutorialを実行する。",
      "Type": "Task",
      "Resource": "${fof_state_translator_arn}",
      "ResultPath": "$.state",
      "Next": "Main"
    },
    "Main": {
      "Type": "Pass",
      "Next": "文脈なしの返答すべき？"
    },
    "文脈なしの返答すべき？": {
      "Comment": "A Choice state adds branching logic to a state machine. Choice rules can implement 16 different comparison operators, and can be combined using And, Or, and Not",
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.IsPreResponse",
          "BooleanEquals": true,
          "Next": "Yes"
        },
        {
          "Variable": "$.IsPreResponse",
          "BooleanEquals": false,
          "Next": "No"
        }
      ],
      "Default": "Yes"
    },
    "Yes": {
      "Type": "Pass",
      "Next": "Intent?"
    },
    "No": {
      "Type": "Pass",
      "Next": "State?"
    },
    "Intent?": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.intent",
          "StringEquals": "UseIntent",
          "Next": "Use"
        }
      ],
      "Default": "文脈なしの返答"
    },
    "Use": {
      "Type": "Task",
      "Resource": "${fof_intent_use_arn}",
      "Next": "PostProcess"
    },
    "文脈なしの返答": {
      "Comment": "A Wait state delays the state machine from continuing for a specified time.",
      "Type": "Task",
      "Resource": "${fof_manual_handler_arn}",
      "Next": "PostProcess"
    },
    "State?": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.state",
          "StringEquals": "Launch",
          "Next": "Launch"
        },
        {
          "Variable": "$.state",
          "StringEquals": "Oracle",
          "Next": "Oracle"
        },
        {
          "Variable": "$.state",
          "StringEquals": "Tutorial",
          "Next": "Tutorial"
        },
        {
          "Variable": "$.state",
          "StringEquals": "Ganesha",
          "Next": "Ganesha"
        },
        {
          "Variable": "$.state",
          "StringEquals": "Use",
          "Next": "Use"
        }
      ],
      "Default": "Launch"
    },
    "Tutorial": {
      "Type": "Task",
      "Resource": "${fof_state_tutorial_arn}",
      "Next": "PostProcess"
    },
    "Launch": {
      "Type": "Task",
      "Resource": "${fof_state_launch_arn}",
      "Next": "PostProcess"
    },
    "Oracle": {
      "Type": "Task",
      "Resource": "${fof_state_oracle_arn}",
      "Next": "PostProcess"
    },
    "Ganesha": {
      "Type": "Task",
      "Resource": "${fof_state_ganesha_shop_arn}",
      "Next": "PostProcess"
    },
    "PostProcess": {
      "Type": "Pass",
      "Next": "TextTranslator"
    },
    "TextTranslator": {
      "Type": "Task",
      "Resource": "${fof_text_translator_arn}",
      "ResultPath": "$.response_text",
      "Next": "StateChanger"
    },
    "StateChanger": {
      "Type": "Task",
      "Resource": "${fof_state_changer_arn}",
      "ResultPath": "$.state",
      "Next": "NodeCleaner"
    },
    "NodeCleaner": {
      "Type": "Task",
      "Resource": "${fof_post_node_cleaner_arn}",
      "ResultPath": "$.node",
      "Next": "SaveAttr"
    },
    "SaveAttr": {
      "Type": "Task",
      "Resource": "${fof_post_save_attr_arn}",
      "ResultPath": null,
      "End": true
    }
  }
}

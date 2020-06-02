{
  "Comment": "A Hello World example demonstrating various state types of the Amazon States Language",
  "StartAt": "StateTranslator",
  "States": {
    "StateTranslator": {
      "Comment": "新規ユーザーはTutorialを実行する。",
      "Type": "Task",
      "Resource": "${fof_state_translator_arn}",
      "ResultPath": "$.state",
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
      "Next": "文脈なしの返答"
    },
    "No": {
      "Type": "Pass",
      "Next": "State?"
    },
    "文脈なしの返答": {
      "Comment": "A Wait state delays the state machine from continuing for a specified time.",
      "Type": "Task",
      "Resource": "${fof_manual_handler_arn}",
      "Next": "StateChanger"
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
        }
      ],
      "Default": "Launch"
    },
    "Tutorial": {
      "Type": "Task",
      "Resource": "${fof_state_tutorial_arn}",
      "Next": "StateChanger"
    },
    "Launch": {
      "Type": "Task",
      "Resource": "${fof_state_launch_arn}",
      "Next": "StateChanger"
    },
    "Oracle": {
      "Type": "Task",
      "Resource": "${fof_state_oracle_arn}",
      "Next": "StateChanger"
    },
    "StateChanger": {
      "Type": "Task",
      "Resource": "${fof_state_changer_arn}",
      "ResultPath": "$.state",
      "End": true
    }
  }
}

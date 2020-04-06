import json


def main(action):
    if action['type'] == 'ask_oracle':
        return 'expect_oracle'
    elif action['type'] == 'launch':
        return 'end'
    return 'そんなステートないですよw'


def lambda_handler(event, context):
    state = main(action=event)
    return state

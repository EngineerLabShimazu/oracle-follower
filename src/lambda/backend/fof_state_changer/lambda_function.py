import json


def main(action):
    if action['type'] == 'ask_oracle':
        return 'expect_oracle'
    elif action['type'] == 'launch':
        return 'end'
    elif action['type'] == 'help':
        return 'oracle'
    elif action['type'] == 'ganesha':
        return 'ganesha'
    elif action['type'] == 'use':
        return 'use'
    return 'そんなステートないですよw'


def lambda_handler(event, context):
    state = main(action=event)
    return state

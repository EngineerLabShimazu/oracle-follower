import json


def main(action):
    if action['type'] == 'oracle':
        return 'oracle'
    elif action['type'] == 'launch':
        return 'end'
    elif action['type'] == 'help':
        return 'oracle'
    elif action['type'] == 'ganesha':
        return 'ganesha'
    elif action['type'] == 'use':
        return 'use'
    elif action['type'] == 'tutorial':
        return 'tutorial'
    return 'そんなステートないですよw'


def lambda_handler(event, context):
    state = main(action=event)
    return state

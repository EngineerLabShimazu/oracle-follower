import json


def main(action):
    if action['type'] == 'oracle':
        return 'Oracle'
    elif action['type'] == 'launch':
        return 'End'
    elif action['type'] == 'help':
        return 'Oracle'
    elif action['type'] == 'ganesha':
        return 'Ganesha'
    elif action['type'] == 'use':
        return 'Use'
    elif action['type'] == 'what_have_i_got':
        return 'WhatHaveIGot'
    elif action['type'] == 'tutorial':
        return 'Tutorial'
    return 'そんなステートないですよw'


def lambda_handler(event, context):
    state = main(action=event)
    return state

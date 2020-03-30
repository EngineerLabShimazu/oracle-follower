from __future__ import print_function
import json

import hero
from dynamo_ctl import DynamoCtl


def main(intent, destination):
    response = {}
    response_text = []

    if intent == 'Destination':
        response_text.append(hero.repeat_oracle(destination))

    response["response_text"] = "".join(response_text)
    return response


def lambda_handler(event, context):
    intent = event['intent']
    destination = event['Destination']
    response = main(intent, destination)
    return response

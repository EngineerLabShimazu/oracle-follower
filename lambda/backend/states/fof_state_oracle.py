from __future__ import print_function

from fof_sdk import hero
from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import user


def main(destination, alexa_user_id):
    action = {'type': 'end'}
    response_text = [hero.repeat_oracle(destination)]
    action["response_text"] = "".join(response_text)

    with DynamoCtl(alexa_user_id) as dynamo_ctl:
        _user = user.get_user(alexa_user_id, dynamo_ctl.attr)
        _user.destination = destination
        print(f'user destination: {_user.destination}')
        dynamo_ctl.attr = _user.attr

    return action


def lambda_handler(event, context):
    destination = event['destination']
    alexa_user_id = event['alexa_user_id']
    response = main(destination, alexa_user_id)
    return response

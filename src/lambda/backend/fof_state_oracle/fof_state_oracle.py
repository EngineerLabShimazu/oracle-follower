from __future__ import print_function

from fof_sdk import hero
from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import user
from fof_sdk import util


def main(destination_intent, alexa_user_id, destinations_choice):
    destination = util.valid_destination(destination_intent)
    if not destination:
        return {'type': 'oracle',
                'response_text': f'大変申し訳ございません。わたくしの理解が及ばず、、、もう一度お告げを頂戴したく存じます。{hero.ask_oracle(destinations_choice)}',
                'set_should_end_session': False}

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
    destinations_choice = event['destinations_choice']
    response = main(destination, alexa_user_id, destinations_choice)
    return response

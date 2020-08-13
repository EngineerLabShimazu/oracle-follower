from __future__ import print_function

from fof_sdk import hero
from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import user
from fof_sdk import util
from fof_sdk import lambda_util


def main(env, destination_intent, alexa_user_id, destinations_choice):
    destination = util.valid_destination(destination_intent)
    if not destination:
        # f'大変申し訳ございません。わたくしの理解が及ばず、、、もう一度お告げを頂戴したく存じます。{hero.ask_oracle(destinations_choice)}'
        return {'type': 'oracle',
                'original_texts': [
                    hero.pardon(),
                    hero.ask_oracle(destinations_choice)
                ],
                'set_should_end_session': False}

    action = {'type': 'end',
              "original_texts": [
                  hero.repeat_oracle(destination)
                  ]
              }

    with DynamoCtl(env, alexa_user_id) as dynamo_ctl:
        _user = user.get_user(alexa_user_id, dynamo_ctl.attr)
        _user.destination = destination

        print(f'user destination: {_user.destination}')
        dynamo_ctl.attr = _user.attr

    return action


def lambda_handler(event, context):
    env = lambda_util.get_env(context)
    alexa_user_id = event['alexa_user_id']
    destination = event.get('destination')
    destinations_choice = event.get('destinations_choice')
    response = main(env, destination, alexa_user_id, destinations_choice)
    return response

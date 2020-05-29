from __future__ import print_function

import random
from fof_sdk import hero
from fof_sdk import user
from fof_sdk import util
from fof_sdk.dynamo_ctl import DynamoCtl


def main(alexa_user_id):
    action = {'type': 'launch'}
    response_texts = [hero.message()]

    with DynamoCtl(alexa_user_id) as dynamo_ctl:
        _user = user.get_user(alexa_user_id, dynamo_ctl.attr)

        if _user.is_first_launch_today:
            if _user.destination:
                response_texts.append(
                    hero.action_report(_user.destination, _user.contents))
                _user.increase_follower()
                response_texts.append(hero.increase_follower(
                    _user.follower_increase, _user.follower_total_amount))

            _user.clear_destination()
            _user.set_event()

        if not _user.has_todays_oracle:
            destinations_choice = random.sample(util.get_village_names(), 2)
            ask_oracle_text = hero.ask_oracle(destinations_choice)
            response_texts.append(ask_oracle_text)
            action = {'type': 'ask_oracle',
                      'set_should_end_session': False,
                      'destinations_choice': destinations_choice}
        dynamo_ctl.attr = _user.attr

    # post process
    # response['response_text'] = ''.join(response_text)

    action['response_text'] = ''.join(response_texts)
    return action


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    response = main(alexa_user_id)
    return response

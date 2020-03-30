from __future__ import print_function
import json

import user
import hero
from dynamo_ctl import DynamoCtl


def main(alexa_user_id):
    response = {}
    response_text = [hero.message()]

    with DynamoCtl(alexa_user_id) as dynamo_ctl:
        _user = user.get_user(alexa_user_id, dynamo_ctl.attr)

        if _user.is_first_launch_today:
            _user.increase_follower()
            response_text.append(hero.increase_follower(
                _user.follower_increase, _user.follower_total_amount))

        if not _user.has_todays_oracle:
            response_text.append(hero.ask_oracle())
            response['state'] = 'oracle'

        dynamo_ctl.attr = _user.attr

    response['response_text'] = ''.join(response_text)
    return response


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    response = main(alexa_user_id)
    return response

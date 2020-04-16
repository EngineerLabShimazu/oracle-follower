from __future__ import print_function

from fof_sdk import hero, user
from fof_sdk.dynamo_ctl import DynamoCtl


def main(alexa_user_id):
    action = {'type': 'launch'}
    response_texts = [hero.message()]

    with DynamoCtl(alexa_user_id) as dynamo_ctl:
        _user = user.get_user(alexa_user_id, dynamo_ctl.attr)

        if _user.is_first_launch_today:
            _user.increase_follower()
            response_texts.append(hero.increase_follower(
                _user.follower_increase, _user.follower_total_amount))

        if not _user.has_todays_oracle:
            ask_oracle_text = hero.ask_oracle()
            response_texts.append(ask_oracle_text)
            action = {'type': 'ask_oracle',
                      'set_should_end_session': False,
                      'ask_oracle_text': ask_oracle_text}
        dynamo_ctl.attr = _user.attr

    # post process
    # response['response_text'] = ''.join(response_text)

    action['response_text'] = ''.join(response_texts)
    return action


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    response = main(alexa_user_id)
    return response

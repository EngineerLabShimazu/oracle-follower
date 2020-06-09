from __future__ import print_function

import random
from fof_sdk import hero
from fof_sdk import user
from fof_sdk import util
from fof_sdk.dynamo_ctl import DynamoCtl


def main(alexa_user_id):
    action = {
        'type': 'launch',
        'image_url': util.get_image('hero_stand')
        }
    original_texts = [hero.message()]

    with DynamoCtl(alexa_user_id) as dynamo_ctl:
        _user = user.get_user(alexa_user_id, dynamo_ctl.attr)

        if _user.is_first_launch_today:
            if _user.destination:
                original_texts.append(
                    hero.action_report(_user.destination, _user.contents))
                _user.increase_follower()
                original_texts.append(hero.increase_follower(
                    _user.follower_increase))
                original_texts.append(hero.total_followers(
                    _user.follower_total_amount))

            # 昨日のお告げによって目的地へは行って帰ってきたのでクリア
            _user.clear_destination()

            # 今日の目的地ガチャ
            _user.set_event()

        if not _user.has_todays_oracle:
            destinations_choice = random.sample(util.get_village_names(), 2)
            ask_oracle_text = hero.ask_oracle(destinations_choice)
            original_texts.append(ask_oracle_text)
            action = {'type': 'ask_oracle',
                      'set_should_end_session': False,
                      'destinations_choice': destinations_choice}
        dynamo_ctl.attr = _user.attr

    action['original_texts'] = original_texts
    return action


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    response = main(alexa_user_id)
    return response

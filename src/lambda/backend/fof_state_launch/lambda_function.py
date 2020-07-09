from __future__ import print_function

import random
from fof_sdk import hero
from fof_sdk.user import User
from fof_sdk import util


def main(user):
    action = {
        'type': 'launch',
        'image_url': util.get_image('hero/hero_stand'),
        'bg_image_url': util.get_image('bg/fof-map')
    }
    original_texts = [hero.message()]

    if user.is_first_launch_today:
        if user.destination:
            original_texts.append(
                hero.action_report(user.destination, user.content))
            user.increase_follower()
            original_texts.append(hero.increase_follower(
                user.follower_increase))
            original_texts.append(hero.total_followers(
                user.follower_total_amount))

        # 昨日のお告げによって目的地へは行って帰ってきたのでクリア
        user.clear_destination()

        # 今日の目的地ガチャ
        user.set_event()

    if not user.has_todays_oracle:
        destinations_choice = random.sample(util.get_village_names(), 2)
        ask_oracle_text = hero.ask_oracle(destinations_choice)
        original_texts.append(ask_oracle_text)
        action = {'type': 'ask_oracle',
                  'set_should_end_session': False,
                  'destinations_choice': destinations_choice,
                  'image_url': util.get_image('hero/hero_stand'),
                  'bg_image_url': util.get_image('bg/fof-map')
                  }

    action['user_attr'] = user.attr
    action['original_texts'] = original_texts
    return action


def lambda_handler(event, context):
    user = User(event['alexa_user_id'], event['dynamo_attr'])
    response = main(user)
    return response

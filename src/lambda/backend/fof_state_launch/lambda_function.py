from __future__ import print_function

import random
from fof_sdk import hero
from fof_sdk.user import User
from fof_sdk import util


def main(user):
    action = {
        'type': 'launch',
        'image_url': util.get_image('hero/hero_stand'),
        'bg_image_url': util.get_image('bg/fof-map-gauss2', extension='.jpg')
    }
    original_texts = [hero.message()]

    if user.is_first_launch_today:
        if user.destination:
            # 昨日の活動報告を聞く
            action_parts = hero.action_report(user.destination, user.content)
            original_texts.append(action_parts['original_texts'])
            action['image_url'] = action_parts['image_url']
            action['bg_image_url'] = action_parts['bg_image_url']

            # 信者を獲得
            user.increase_follower()
            original_texts.append(hero.increase_follower(
                user.follower_increase))
            original_texts.append(hero.total_followers(
                user.follower_total_amount))

        # 昨日のお告げによって目的地へは行って帰ってきたのでクリア
        user.clear_destination()

        # 今日の目的地ガチャ
        user.set_event()

    if user.has_todays_oracle:
        original_texts.append({
            'text': '本日は「グリーンスター」へ向かうお告げを完了しています。'
        })
        original_texts.append({
            'text': 'クロノスチケットを使い、下界の時間を１日経過させ、すぐに勇者から報告を聞きますか？'
        })
        action['type'] = 'use'
        action['set_should_end_session'] = False

    else:
        destinations_choice = random.sample(util.get_village_names(), 2)
        ask_oracle_text = hero.ask_oracle(destinations_choice)
        original_texts.append(ask_oracle_text)
        action = {'type': 'ask_oracle',
                  'set_should_end_session': False,
                  'destinations_choice': destinations_choice,
                  'image_url': action.get('image_url',
                                          util.get_image('hero/hero_stand')),
                  'bg_image_url': action.get(
                      'bg_image_url', util.get_image(
                          'bg/fof-map-gauss2', extension='.jpg'))
                  }

    action['user_attr'] = user.attr
    action['original_texts'] = original_texts
    return action


def lambda_handler(event, context):
    user = User(event['alexa_user_id'], event['dynamo_attr'])
    response = main(user)
    return response

from __future__ import print_function

import random
import launch_nodes as nodes
from fof_sdk import hero
from fof_sdk.user import User
from fof_sdk import util


def has_chronus_ticket(user: User):
    amount: int = user.get_item('chronus_ticket')
    if not amount:
        return False
    if amount <= 0:
        return False
    return True


def main(user, node, intent):
    action = {
        'type': 'launch',
        'image_url': util.get_image('hero/hero_stand'),
        'bg_image_url': util.get_image('bg/fof-map-gauss2', extension='.jpg')
    }

    if node == 'buy_ticket':
        if intent in ['AMAZON.YesIntent', 'BuyIntent']:
            return nodes.ganesha()
        elif intent == 'AMAZON.NoIntent':
            return nodes.end()
        else:
            return nodes.re_ask()

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
            'text': f'本日は「{user.destination}」へ向かうお告げを完了しています。'
        })
        if has_chronus_ticket(user):
            original_texts.append({
                'text': 'CONFIRM_CHRONUS_TICKET'
            })
            action['type'] = 'use'
            action['node'] = 'use_ticket'
        else:
            original_texts.append({
                'text': 'RECOMMEND_CHRONUS_TICKET'
            })
            action['type'] = 'launch'
            action['node'] = 'buy_ticket'
        action['set_should_end_session'] = False

    else:
        destinations_choice = random.sample(util.get_village_names(), 2)
        ask_oracle_text = hero.ask_oracle(destinations_choice)
        original_texts.append(ask_oracle_text)
        action = {'type': 'oracle',
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
    node = event.get('node')
    intent = event.get('intent')
    response = main(user, node, intent)
    return response

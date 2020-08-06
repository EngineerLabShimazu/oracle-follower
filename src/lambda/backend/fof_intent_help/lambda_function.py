import random

from fof_sdk import util
from fof_sdk import hero
from fof_sdk.user import User


def has_chronus_ticket(user: User):
    amount: int = user.get_item('chronus_ticket')
    if not amount:
        return False
    if amount <= 0:
        return False
    return True


def add_item_text(ticket_amount):
    if ticket_amount <= 0:
        return {'text': 'アイテムは所持していません。'}
    return {'text': f'クロノスチケットを{ticket_amount}枚持っています。'}


def main(user, destinations):
    action = {
        'type': 'help',
        'image_url': util.get_image('hero/hero_stand'),
        'bg_image_url': util.get_image('bg/fof-map-gauss2', extension='.jpg')
    }
    ticket_amount: int = user.get_item('chronus_ticket', 0)
    original_texts = [{'text': 'SKILL_SUMMARY'},
                      {
                          'text': 'CURRENT_GEM',
                          'kwargs': {
                              'paid_gem': user.paid_gem,
                              'free_gem': user.free_gem
                          }
                      },
                      add_item_text(ticket_amount)
                      ]

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
            action['type'] = 'ganesha'
            action['node'] = 'launch'
    else:
        if not destinations:
            destinations = random.sample(util.get_village_names(), 2)
        original_texts.append(hero.total_followers(user.follower_total_amount))
        original_texts.append(hero.ask_oracle(destinations))
    action['original_texts'] = original_texts
    return action


def tutorial_salvation():
    return {
        'type': 'tutorial',
        'node': 'salvation',
        'image_url': util.get_image('gods/greatest-god'),
        'bg_image_url': util.get_image('bg/fof-map-gauss2', extension='.jpg'),
        'original_texts': [
            {
                'text': 'HELP_TUTORIAL_SALVATION',
            }
        ]
    }


def tutorial_send_out():
    return {
        'type': 'tutorial',
        'node': 'send_out',
        'image_url': util.get_image('gods/greatest-god'),
        'bg_image_url': util.get_image('bg/fof-map-gauss2', extension='.jpg'),
        'original_texts': [
            {
                'text': 'HELP_TUTORIAL_SEND_OUT',
            }
        ]
    }


def lambda_handler(event, context):
    destinations = event.get('destinations_choice')
    user = User(event['alexa_user_id'], event['dynamo_attr'])
    state = event.get('state')
    node = event.get('node')
    if state == 'Tutorial' and node == 'salvation':
        return tutorial_salvation()
    elif state == 'Tutorial' and node == 'send_out':
        return tutorial_send_out()
    response = main(user, destinations)
    return response

import random
from typing import Optional

import nodes
from gatcha_items import gatcha_items
from fof_sdk import util
from fof_sdk.user import User


def draw_lottery():
    item_name_list = []
    weight_list = []
    for k, item in gatcha_items.items():
        item_name_list.append(item['name'])
        weight_list.append(item['ratio'])

    item = random.choices(item_name_list, weight_list)[0]
    return item


def gatcha(turn_times):
    items = []
    for i in range(turn_times):
        items.append(draw_lottery())
    return items


def change_node(node_key, accept: bool, is_paid: Optional[bool]):
    if node_key == 'launch':
        return 'welcome'
    elif node_key == 'welcome':
        if is_paid is False:
            return 'recommend_gem'
        elif accept and is_paid:
            return 'gatcha'
        return 'recommend_gatcha'
    elif node_key == 'recommend_gatcha':
        if is_paid is False:
            return 'recommend_gem'
        elif accept and is_paid:
            return 'gatcha'
        return 'end'
    elif node_key == 'gatcha':
        if is_paid is False:
            return 'recommend_gem'
        elif accept:
            return 'gatcha'
        return 'end'
    elif node_key == 'result':
        return 'gatcha' if accept else 'end'


def should_gatcha(turn_times):
    return bool(turn_times)


def set_gatcha_result(user, item, add_amount):
    amount: int = user.get_item(item, 0)
    user.set_item('chronus_ticket', amount + add_amount)


def re_ask(node, turn_times):
    action = {
        'type': 'ganesha',
        'image_url': util.get_image('gods/ganesha'),
        'bg_image_url': util.get_image('bg/ganesha-shop',
                                       extension='.jpg'),
        'set_should_end_session': False
    }

    if node == 'welcome':
        text = nodes.recommend_ten()
    if node == 'recommend_gatcha':
        text = nodes.recommend_gatcha()
    action.update(text)
    return action


def main(turn_times, node_key, user, total_ticket_amount):
    action = {
        'type': 'ganesha',
        'image_url': util.get_image('gods/ganesha'),
        'bg_image_url': util.get_image('bg/ganesha-shop',
                                       extension='.jpg'),
        'set_should_end_session': False
    }

    if node_key == 'launch':
        node = nodes.launch()
    elif node_key == 'welcome':
        if should_gatcha(turn_times):
            gem_amount_map = {
                1: 300,
                10: 3000
            }
            is_paid = user.pay_gem(gem_amount_map[turn_times])
            if is_paid:
                items = gatcha(turn_times)
                node = nodes.gatcha(turn_times, items, user)
            else:
                node = nodes.recommend_gem(turn_times)
            node['is_paid'] = is_paid
        else:
            node = nodes.recommend_gatcha()
    elif node_key == 'recommend_gatcha':
        if should_gatcha(turn_times):
            gem_amount_map = {
                1: 300,
                10: 3000
            }
            is_paid = user.pay_gem(gem_amount_map[turn_times])
            if is_paid:
                items = gatcha(turn_times)
                node = nodes.gatcha(turn_times, items, user)
            else:
                node = nodes.recommend_gem(turn_times)
            node['is_paid'] = is_paid
        else:
            node = nodes.end()
    elif node_key == 'gatcha':
        if should_gatcha(turn_times):
            gem_amount_map = {
                1: 300,
                10: 3000
            }
            is_paid = user.pay_gem(gem_amount_map[turn_times])
            if is_paid:
                items = gatcha(turn_times)
                node = nodes.gatcha(turn_times, items, user)
            else:
                node = nodes.recommend_gem(turn_times)
            node['is_paid'] = is_paid
        else:
            node = nodes.end()
    elif node_key == 'result':
        node = nodes.result(total_ticket_amount, turn_times, user)
    else:
        node = {
            'original_texts': [
                {
                    'text': ''
                }
            ]
        }

    # lambdaのインプットであるturn_timesよりも、nodes.pyで指定しているturn_timesを優先する。
    accept = bool(node.get('turn_times', turn_times))
    is_paid = node.get('is_paid')

    total_ticket_amount = node.get('total_ticket_amount')
    if total_ticket_amount:
        set_gatcha_result(user, 'chronus_ticket', total_ticket_amount)

    node['node'] = change_node(node_key, accept, is_paid)

    action.update(node)
    action['user_attr'] = user.attr

    return action


def lambda_handler(event, context):
    turn_times = event.get('turn_times')
    user = User(event['alexa_user_id'], event['dynamo_attr'])
    total_ticket_amount = event.get('total_ticket_amount', 0)
    node_key = event.get('node', 'launch')

    intent = event.get('intent')
    if intent == 'AMAZON.NoIntent':
        turn_times = 0

    valid_intents = ['AMAZON.YesIntent', 'AMAZON.NoIntent',
                     'TurnIntent', 'TurnTimesIntent']

    if node_key in ['welcome', 'recommend_gatcha']:
        if intent not in valid_intents:
            return re_ask(node_key, turn_times)

    if node_key in ['result', 'gatcha']:
        if intent not in valid_intents:
            node_key = 'result'

    response = main(turn_times, node_key, user, total_ticket_amount)
    return response

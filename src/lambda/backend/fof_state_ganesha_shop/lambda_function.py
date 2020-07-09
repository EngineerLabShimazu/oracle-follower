import random
import nodes
from gatcha_items import gatcha_items
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
    if turn_times == 1:
        draw_lottery()
    if turn_times == 10:
        pass


def change_node(node_key, accept):
    if node_key == 'launch':
        return 'welcome'
    elif node_key == 'welcome':
        return 'gatcha' if accept else 'recommend_gatcha'
    elif node_key == 'recommend_gatcha':
        return 'gatcha' if accept else 'end'
    elif node_key == 'gatcha':
        return 'gatcha' if accept else 'end'


def should_gatcha(turn_times):
    return bool(turn_times)


def main(turn_times, node_key, user):

    action = {'type': 'ganesha'}

    if node_key == 'launch':
        node = nodes.launch()
    elif node_key == 'welcome':
        if should_gatcha(turn_times):
            node = nodes.gatcha(turn_times)
        else:
            node = nodes.recommend_gatcha()
    elif node_key == 'recommend_gatcha':
        if should_gatcha(turn_times):
            node = nodes.gatcha(turn_times)
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
                node = nodes.gatcha(turn_times)
            else:
                node = nodes.recommend_gem(turn_times)
        else:
            node = nodes.end()
    else:
        node = {
            'original_texts': [
                {
                    'text': ''
                }
            ]
        }

    # nodeのturn_timesを優先する。
    accept = bool(node.get('turn_times', turn_times))
    node['node'] = change_node(node_key, accept)

    action.update(node)

    return action


def lambda_handler(event, context):
    turn_times = event.get('turn_times')
    node_key = event.get('node', 'launch')
    user = User(event['alexa_user_id'], event['dynamo_attr'])
    response = main(turn_times, node_key, user)
    return response

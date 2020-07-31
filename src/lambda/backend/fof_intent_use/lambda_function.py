import intent_use_nodes as nodes
from fof_sdk.user import User


def main(node, user, intent):
    if intent not in ['Amazon.YesIntent', 'UseIntent']:
        return nodes.re_ask()
    _node_map = {
        'launch': nodes.launch,
        'use_ticket': nodes.use_ticket
    }
    node_handler = _node_map.get(node)
    return node_handler(user, intent)


def lambda_handler(event, context):
    node = event.get('node', 'launch')
    user = User(event['alexa_user_id'], event['dynamo_attr'])
    intent = event.get('intent')
    response = main(node, user, intent)
    return response

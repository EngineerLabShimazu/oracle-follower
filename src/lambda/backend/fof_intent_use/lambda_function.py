import intent_use_nodes as nodes
from fof_sdk.user import User
from fof_sdk import hero
from fof_sdk import util


def main(node, user, intent):
    if intent == 'AMAZON.NoIntent':
        return {
            'type': 'cancel_or_stop',
            'image_url': util.get_image('hero/hero_anticipation'),
            'bg_image_url': util.get_image(
                'bg/fof-map-gauss2', extension='.jpg'),
            'original_texts': [
                {
                    'text': 'APPRECIATE_ON_STOP',
                    'kwargs': {
                        'appreciate': hero.get_appreciate_message()
                    }
                },
                {
                    'text': 'PLEASE_AGAIN_ON_STOP'
                }
            ]
        }
    if intent not in ['AMAZON.YesIntent', 'UseIntent']:
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

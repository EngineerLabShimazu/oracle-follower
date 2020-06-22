import random
from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import user
from fof_sdk import hero
from fof_sdk import util


def main(alexa_user_id, intent, destinations, product_reference_name):
    action = {
        'type': 'end'
        }
    if intent == 'HelpIntent':
        with DynamoCtl(alexa_user_id) as dynamo_ctl:
            _user = user.get_user(alexa_user_id, dynamo_ctl.attr)
            dynamo_ctl.attr = _user.attr

            if not destinations:
                destinations = random.sample(util.get_village_names(), 2)
            return {
                'type': 'help',
                'original_texts': [
                    {'text': 'SKILL_SUMMARY'},
                    hero.total_followers(_user.follower_total_amount),
                    hero.ask_oracle(destinations)
                    ]
                }
    elif intent == 'CancelOrStopIntent':
        return {
            'type': 'cancel_or_stop',
            'image_url': util.get_image('hero/hero_anticipation'),
            'bg_image_url': util.get_image('bg/fof-map'),
            'original_texts': [
                {
                    'text': 'APPRECIATE_ON_STOP',
                    'kwargs': {
                        'appreciate': hero.get_appreciate_message()
                        }
                    },
                {'text': 'PLEASE_AGAIN_ON_STOP'}
                ]
            }
    elif intent == 'Connections.Response':
        if not product_reference_name:
            return {
                'type': 'Connections.Response',
                'original_texts': [
                    {
                        'text': 'ASK_GO_TO_GANESHA_SHOP'
                        }
                    ]
                }
        with DynamoCtl(alexa_user_id) as dynamo_ctl:
            _user = user.get_user(alexa_user_id, dynamo_ctl.attr)
            added = _user.add_gem(product_reference_name)
            if not added:
                return {
                    'type': 'Connections.Response',
                    'original_texts': [
                        {
                            'text': 'ASK_GO_TO_GANESHA_SHOP'
                            }
                        ]
                    }
            dynamo_ctl.attr = _user.attr
        return {
            'type': 'Connections.Response',
            'original_texts': [
                {
                    'text': 'ADD_GEM',
                    'kwargs': {
                        'paid_gem': added['paid_gem'],
                        'free_gem': added['free_gem']
                        }
                    },
                {
                    'text': 'CURRENT_GEM',
                    'kwargs': {
                        'paid_gem': _user.paid_gem,
                        'free_gem': _user.free_gem
                        }
                    },
                {
                    'text': 'ASK_GO_TO_GANESHA_SHOP'
                    }
                ]
            }
    return action


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    intent = event['intent']
    destinations = event.get('destinations_choice')
    product_reference_name = event.get('product_reference_name')
    response = main(alexa_user_id, intent, destinations,
                    product_reference_name)
    return response

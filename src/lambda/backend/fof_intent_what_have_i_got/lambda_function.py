import nodes
from fof_sdk import util
from fof_sdk.user import User


def main(user):
    action = {
        'type': 'what_have_i_got',
        'image_url': util.get_image('hero/hero_stand'),
        'bg_image_url': util.get_image('bg/fof-map-gauss2', extension='.jpg')
    }

    paid_gem = user.paid_gem
    free_gem = user.free_gem
    original_texts = [{
        'text': 'USER_GEMS',
        'kwargs': {
            'paid_gem': paid_gem,
            'free_gem': free_gem
        }
    }]

    total_gem = paid_gem + free_gem
    if total_gem >= 300:
        original_texts.append({
            'text': 'ASK_GANESHA'
        })
        action['node'] = 'ask_ganesha'
    else:
        original_texts.append({
            'text': 'ASK_GEM_PACK'
        })
        action['node'] = 'ask_gem_pack'
        action['product_name'] = 'gem_1000'

    action['original_texts'] = original_texts
    return action


def lambda_handler(event, context):
    user = User(event['alexa_user_id'], event['dynamo_attr'])
    intent = event.get('intent')

    if intent not in ['AMAZON.YesIntent', 'AMAZON.NoIntent', 'BuyIntent']:
        node = event.get('node')
        return nodes.reask(node)

    response = main(user)
    return response

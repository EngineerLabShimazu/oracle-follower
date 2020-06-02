from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import user
from fof_sdk import hero
from fof_sdk import util


def main(alexa_user_id, intent, destinations):
    action = {
        'type': 'end'
        }
    if intent == 'HelpIntent':
        with DynamoCtl(alexa_user_id) as dynamo_ctl:
            _user = user.get_user(alexa_user_id, dynamo_ctl.attr)
            follower_summary_recommend = f'現在の合計は{_user.follower_total_amount}人です。' if _user.follower_total_amount > 0 else ''
            dynamo_ctl.attr = _user.attr
            return {
                'type': 'help',
                'response_text': '「お告げの勇者」では、この世界の神であるあなたのお告げによって勇者を成長させ、あなたの信者数を拡大していただきます。'
                                 f'{follower_summary_recommend}'
                                 f'本日勇者は、{destinations[0]}と{destinations[1]}のどちらへ向かえばよろしいでしょうか?'
                }
    elif intent == 'CancelOrStopIntent':
        return {
            'type': 'cancel_or_stop',
            'response_text': f'本日も{hero.get_appreciate_message()}、ありがとうございました。'
                             f'また信仰を捧げさせていただく機会を、どうか、お与えくださいませ。',
            'image_url': util.get_image('hero_anticipation')
            }
    return action


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    intent = event['intent']
    destinations = event.get('destinations_choice')
    response = main(alexa_user_id, intent, destinations)
    return response

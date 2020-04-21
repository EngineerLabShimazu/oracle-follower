from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import user


def main(alexa_user_id, intent, destinations):
    action = {
        'type': 'end'
        }
    if intent == 'HelpIntent':
        with DynamoCtl(alexa_user_id) as dynamo_ctl:
            _user = user.get_user(alexa_user_id, dynamo_ctl.attr)
            follower_summary_recommend = f'現在の合計は{_user.follower_total_amount}人です。' if _user.follower_total_amount > 0 else ''
            return {
                'type': 'help',
                'response_text': '「お告げの勇者」では、この世界の神であるあなたのお告げによって勇者を成長させ、あなたの信者数を拡大していただきます。'
                                 f'{follower_summary_recommend}'
                                 f'本日勇者は、{destinations[0]}と{destinations[1]}のどちらへ向かえばよろしいでしょうか?'
                }
    return action


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    intent = event['intent']
    destinations = event['destinations']
    response = main(alexa_user_id, intent, destinations)
    return response

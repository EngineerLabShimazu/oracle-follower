import nodes
from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import user


def main(alexa_user_id, node_key, destination):
    action = {
        'type': 'tutorial',
        'set_should_end_session': False
        }
    if node_key == 'launch':
        node = nodes.launch()
    elif node_key == 'salvation':
        node = nodes.salvation()
    elif node_key == 'send_out':
        node = nodes.send_out(destination)
    else:
        node = {
            'original_texts': [
                {
                    'text': ''
                    }
                ]
            }
    action.update(node)

    if action.get('end'):
        action['set_should_end_session'] = True

        with DynamoCtl(alexa_user_id) as dynamo_ctl:
            # tutorial が終わったら、last_launch_date を入れ、
            # skill 初回起動判定をFalseにする
            _user = user.get_user(alexa_user_id, dynamo_ctl.attr)
            _user.destination = destination

            # 目的地ガチャ
            _user.set_event()
            dynamo_ctl.attr = _user.attr
    return action


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    node_key = event.get('node', 'launch')
    destination = event.get('destination')
    action = main(alexa_user_id, node_key, destination)
    return action

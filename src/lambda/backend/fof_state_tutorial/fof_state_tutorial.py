from nodes import node_map
from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import user


def main(alexa_user_id, node_key):
    action = {
        'type': 'tutorial',
        'set_should_end_session': False
        }
    node = node_map.get(node_key)
    action['response_text'] = ''.join(node['text'])
    action['node'] = node.get('next_node', '')

    if node.get('end'):
        action['set_should_end_session'] = True

        with DynamoCtl(alexa_user_id) as dynamo_ctl:
            # tutorial が終わったら、last_launch_date を入れ、
            # skill 初回起動判定をFalseにする
            _user = user.get_user(alexa_user_id, dynamo_ctl.attr)
            dynamo_ctl.attr = _user.attr
    return action


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    node_key = event.get('node', 'launch')
    action = main(alexa_user_id, node_key)
    return action

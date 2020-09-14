from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import user
from fof_sdk import lambda_util


def main(env, alexa_user_id, node: str, intent: str):
    with DynamoCtl(env, alexa_user_id) as dynamo_ctl:
        _user = user.get_user(alexa_user_id, dynamo_ctl.attr)
        if _user.is_first_launch_skill():
            return 'Tutorial', ''
        if (node == 'ask_ganesha' or node == 'ask_gem_pack') \
                and intent == 'AMAZON.NoIntent':
            return 'Launch', ''
        if node == 'ask_ganesha' and intent == 'AMAZON.YesIntent':
            return 'Ganesha', 'launch'
    return '', ''


def lambda_handler(event, context):
    env = lambda_util.get_env(context)
    _alexa_user_id = event['alexa_user_id']
    _state = event.get('state', '')
    if not _state:
        return event
    _node = event.get('node', '')
    _intent = event.get('intent', '')
    state, node = main(env, _alexa_user_id, _node, _intent)

    if state:
        event['state'] = state
    if node:
        event['node'] = node

    return event

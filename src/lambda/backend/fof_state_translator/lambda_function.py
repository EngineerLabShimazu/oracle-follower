from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import user
from fof_sdk import lambda_util


def main(env, alexa_user_id, state: str) -> str:
    with DynamoCtl(env, alexa_user_id) as dynamo_ctl:
        _user = user.get_user(alexa_user_id, dynamo_ctl.attr)
        if _user.is_first_launch_skill():
            return 'Tutorial'
    return state


def lambda_handler(event, context):
    env = lambda_util.get_env(context)
    alexa_user_id = event['alexa_user_id']
    _state = event.get('state', '')
    if not _state:
        return
    state = main(env, alexa_user_id, _state)
    return state.capitalize()

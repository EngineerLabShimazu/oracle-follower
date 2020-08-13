from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import lambda_util


def lambda_handler(event, context):
    env = lambda_util.get_env(context)
    user_attr = event.get('user_attr')
    if user_attr:
        with DynamoCtl(env, user_attr['alexa_user_id']) as dynamo_ctl:
            dynamo_ctl.attr = user_attr

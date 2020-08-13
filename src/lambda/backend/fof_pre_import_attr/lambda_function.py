from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import lambda_util


def lambda_handler(event, context):
    env = lambda_util.get_env(context)
    with DynamoCtl(env, event['alexa_user_id']) as dynamo_ctl:
        return dynamo_ctl.attr

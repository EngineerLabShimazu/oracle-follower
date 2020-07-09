from fof_sdk.dynamo_ctl import DynamoCtl


def lambda_handler(event, _):
    with DynamoCtl(event['alexa_user_id']) as dynamo_ctl:
        return dynamo_ctl.attr

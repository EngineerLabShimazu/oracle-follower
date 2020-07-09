from fof_sdk.dynamo_ctl import DynamoCtl


def lambda_handler(event, _):
    user_attr = event.get('user_attr')
    if user_attr:
        with DynamoCtl(event['alexa_user_id']) as dynamo_ctl:
            dynamo_ctl.attr = user_attr

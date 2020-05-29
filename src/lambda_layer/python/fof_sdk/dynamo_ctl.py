import os
import boto3
import boto3.dynamodb.types as dynamodb_types

dynamo = boto3.client('dynamodb')

TABLE_NAME = 'fof_user_prd'
if os.environ.get('AWS_LAMBDA_FUNCTION_VERSION') == '$LATEST':
    TABLE_NAME = 'fof_user_stg'


class DynamoCtl:
    def __init__(self, alexa_user_id):
        self.alexa_user_id = alexa_user_id

        _attr = _get_attr(alexa_user_id)
        if not _attr:
            _attr = {
                'last_launch_date': '',
                'follower_total_amount': 0,
                'follower_increase': 0
                }
        self._attr = _attr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        save_attr(self.alexa_user_id, self.attr)

    @property
    def attr(self):
        return self._attr

    @attr.setter
    def attr(self, value):
        d = {}
        for k, v in value.items():
            if v:
                d[k] = v
        self._attr = d


def _serialize_attribute(attributes):
    return dynamodb_types.TypeSerializer().serialize(attributes)


def _get_attr(user_id):
    """
    :return:
        attr = {
            'last_launch_date': 'YYYY-mm-dd',
            'follower_total_amount': -1,
            'follower_increase': -1
            }
    """
    print(f'table_name {TABLE_NAME}')

    item = dynamo.get_item(TableName=TABLE_NAME,
                           Key={'alexa_user_id': {'S': user_id}}
                           ).get('Item')
    if not item:
        return None
    return dynamodb_types.TypeDeserializer().deserialize(item['attributes'])


def save_attr(alexa_user_id, attributes):
    item = {'alexa_user_id': _serialize_attribute(alexa_user_id),
            'attributes': _serialize_attribute(attributes)}
    dynamo.put_item(TableName=TABLE_NAME,
                    Item=item)

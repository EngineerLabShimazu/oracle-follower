import boto3
import boto3.dynamodb.types as dynamodb_types

dynamo = boto3.client('dynamodb')


class DynamoCtl:
    def __init__(self, alexa_user_id):
        self.alexa_user_id = alexa_user_id
        self.attr = _get_attr(alexa_user_id)


def serialize_attribute(attributes):
    return dynamodb_types.TypeSerializer().serialize(attributes)


def _get_attr(user_id):
    """
    :return:
        attr = {
            'when': {
                'YYYY-mm-dd': {
                    'follower_increase': -1,
                    'follower_total_amount': -1,
                    'destination': 'village_a',
                    }
                },
            'last_launch_date': 'YYYY-mm-dd'
            }
    """
    item = dynamo.get_item(TableName='funDom-oracle-follower-user',
                           Key={'alexa_user_id': {'S': user_id}}
                           )['Item']
    return dynamodb_types.TypeDeserializer().deserialize(item['attributes'])


def set_attr(alexa_user_id, attributes):
    item = {'alexa_user_id': serialize_attribute(alexa_user_id),
            'attributes': serialize_attribute(attributes)}
    dynamo.put_item(TableName='funDom-oracle-follower-user',
                    Item=item)
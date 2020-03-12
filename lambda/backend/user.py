import boto3
import boto3.dynamodb.types as dynamodb_types

dynamo = boto3.client('dynamodb')


def format_attribute(attributes):
    return dynamodb_types.TypeSerializer().serialize(attributes)


def get_user(user_id):
    item = dynamo.get_item(TableName='funDom-oracle-follower-user',
                           Key={'alexa_user_id': {'S': user_id}}
                           )['Item']
    return item


def set_user(alexa_user_id, attributes):
    item = {'alexa_user_id': format_attribute(alexa_user_id),
            'attributes': format_attribute(attributes)}
    dynamo.put_item(TableName='funDom-oracle-follower-user',
                    Item=item)

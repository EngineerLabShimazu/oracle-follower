import boto3
import boto3.dynamodb.types as dynamodb_types
import datetime

dynamo = boto3.client('dynamodb')


def _get_attr(user_id):
    item = dynamo.get_item(TableName='funDom-oracle-follower-user',
                           Key={'alexa_user_id': {'S': user_id}}
                           )['Item']
    return dynamodb_types.TypeDeserializer().deserialize(item['attributes'])


def _get_user(user_id, date):
    attr = _get_attr(user_id)
    return attr[date]


def _set_user(alexa_user_id, attributes):
    item = {'alexa_user_id': serialize_attribute(alexa_user_id),
            'attributes': serialize_attribute(attributes)}
    dynamo.put_item(TableName='funDom-oracle-follower-user',
                    Item=item)


def serialize_attribute(attributes):
    return dynamodb_types.TypeSerializer().serialize(attributes)


class User:
    def __init__(self, alexa_user_id):
        self.alexa_user_id = alexa_user_id
        _user = _get_user(alexa_user_id)
        self.follower_increase = _user['follower_increase']
        self.follower_total_amount = _user['follower_total_amount']
        self.destination = _user['destination']
        self.last_launch_date = _user['last_launch_date']

    def __del__(self):
        _set_user(self.alexa_user_id, {self.__dict__})

    def get_attributes(self):
        return {'attr': self.__dict__}

    def is_first_launch(self):
        today = datetime.date.today().isoformat()
        last_launch = self.last_launch_date
        if today != last_launch:
            return True
        return False

# def increase_follower(self):

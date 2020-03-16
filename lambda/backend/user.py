import boto3
import boto3.dynamodb.types as dynamodb_types
import datetime
import random

dynamo = boto3.client('dynamodb')


class User:
    def __init__(self, alexa_user_id, attr, when=''):
        self.alexa_user_id = alexa_user_id
        self.last_launch_date = attr['last_launch_date']

        _attr = attr['when'][when] if when \
            else attr['when'][self.last_launch_date]

        self.follower_increase: int = _attr['follower_increase']
        self.follower_total_amount: int = _attr['follower_total_amount']
        self.destination: str = _attr['destination']

    def __del__(self):
        _set_user(self.alexa_user_id, {self.__dict__})

    @property
    def attributes(self) -> dict:
        return {'attr': self.__dict__}

    @property
    def is_first_launch_today(self) -> bool:
        today = datetime.date.today().isoformat()
        last_launch = self.last_launch_date
        if today != last_launch:
            return True
        return False

    def increase_follower(self):
        self.follower_increase = random.choice([i for i in range(1, 10)])
        self.follower_total_amount += self.follower_increase


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


def get_user(alexa_user_id) -> User:
    attr = _get_attr(alexa_user_id)
    return User(alexa_user_id, attr)


def _set_user(alexa_user_id, attributes):
    item = {'alexa_user_id': serialize_attribute(alexa_user_id),
            'attributes': serialize_attribute(attributes)}
    dynamo.put_item(TableName='funDom-oracle-follower-user',
                    Item=item)

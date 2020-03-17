import boto3
import boto3.dynamodb.types as dynamodb_types
import datetime
import random

from dynamo_ctl import DynamoCtl, set_attr

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
        self._when = when

    def __del__(self):
        set_user(self.alexa_user_id, self.__dict__, self._when)

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


def get_user(alexa_user_id) -> User:
    attr = DynamoCtl(alexa_user_id).attr
    return User(alexa_user_id, attr)


def set_user(alexa_user_id, user_attr, when=''):
    _when = when if when else user_attr['last_launch_date']
    attr = {
        'when': {
            _when: {
                'follower_increase': user_attr['follower_increase'],
                'follower_total_amount': user_attr['follower_total_amount'],
                'destination': user_attr['destination'],
            }
        },
        'last_launch_date': user_attr['last_launch_date']
    }
    set_attr(alexa_user_id, attr)

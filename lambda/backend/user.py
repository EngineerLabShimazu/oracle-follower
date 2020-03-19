import boto3
import boto3.dynamodb.types as dynamodb_types
import random

from dynamo_ctl import DynamoCtl, set_attr
from util import iso_formatted_date_today

dynamo = boto3.client('dynamodb')


class User:
    def __init__(self, alexa_user_id, attr, when=''):
        self.alexa_user_id = alexa_user_id
        self.last_launch_date = attr.get('last_launch_date')

        _attr = attr['when'][when] if when \
            else attr['when'][iso_formatted_date_today]

        self.follower_increase: int = _attr.get('follower_increase', 0)
        self.follower_total_amount: int = _attr.get('follower_total_amount', 0)
        self.destination: str = _attr.get('destination', '')
        self._when = when

    def __del__(self):
        print('del')
        print(self.__dict__)
        d = {}
        for k, v in self.__dict__.items():
            if v:
                d[k] = v
        set_user(self.alexa_user_id, d, self._when)

    @property
    def attributes(self) -> dict:
        return {'attr': self.__dict__}

    @property
    def is_first_launch_today(self) -> bool:
        if not self.last_launch_date:
            return True
        if iso_formatted_date_today != self.last_launch_date:
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
    last_launch_date = when if when \
        else user_attr.get('last_launch_date', iso_formatted_date_today)
    attr = {
        'when': {
            last_launch_date: {
                }
            },
        'last_launch_date': last_launch_date
        }
    for attribute in user_attr.keys():
        attr['when'][last_launch_date][attribute] = attribute
    set_attr(alexa_user_id, attr)

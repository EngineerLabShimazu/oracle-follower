import boto3
import boto3.dynamodb.types as dynamodb_types
import random

from fof_sdk.util import iso_formatted_date_today

dynamo = boto3.client('dynamodb')


class User:
    def __init__(self, alexa_user_id, attr):
        self.alexa_user_id: str = alexa_user_id
        self.follower_total_amount: int = attr.get('follower_total_amount', 0)
        self.last_launch_date: str = attr.get('last_launch_date', '')
        self.follower_increase: int = attr.get('follower_increase', 0)
        self.destination: str = attr.get('destination', '')

    @property
    def attr(self) -> dict:
        _attr = dict(self.__dict__)
        _attr['last_launch_date'] = iso_formatted_date_today
        return _attr

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

    def has_todays_oracle(self):
        if self.destination:
            return True
        return False


def serialize_attribute(attributes):
    return dynamodb_types.TypeSerializer().serialize(attributes)


def get_user(alexa_user_id, attr) -> User:
    return User(alexa_user_id, attr)
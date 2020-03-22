import boto3
import boto3.dynamodb.types as dynamodb_types
import random

from util import iso_formatted_date_today

dynamo = boto3.client('dynamodb')


class User:
    def __init__(self, alexa_user_id, attr):
        self.alexa_user_id: str = alexa_user_id
        self.follower_total_amount: int = attr.get('follower_total_amount', 0)
        self.last_launch_date: str = attr.get('last_launch_date', '')
        self.follower_increase = attr.get('follower_increase', 0)

    @property
    def attributes(self) -> dict:
        self.last_launch_date = iso_formatted_date_today
        return self.__dict__

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


def get_user(alexa_user_id, attr) -> User:
    return User(alexa_user_id, attr)

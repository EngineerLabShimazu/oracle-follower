import boto3
import boto3.dynamodb.types as dynamodb_types
import random

# from dynamo_ctl import DynamoCtl, set_attr
from util import iso_formatted_date_today

dynamo = boto3.client('dynamodb')


class User:
    def __init__(self, alexa_user_id, attr, when=''):
        # 記録
        if attr.get('last_launch_date', '') == iso_formatted_date_today:
            # 今日すでに情報を持っていたら取りたい
            today_attr = attr['when'][iso_formatted_date_today]
            self.follower_increase: int = today_attr.get('follower_increase', 0)
            self.destination: str = today_attr.get('destination', '')

        # 永続
        self.alexa_user_id: str = alexa_user_id
        self.follower_total_amount: int = attr.get('follower_total_amount', 0)
        self.last_launch_date: str = attr.get('last_launch_date', '')
        self._when = when

    def __del__(self):
        print('del')
        print(self.__dict__)
        d = {}
        for k, v in self.__dict__.items():
            if v:
                d[k] = v
        # set_user(self.alexa_user_id, d)

    @property
    def when_attr(self):
        return {
            'follower_increase': self.follower_increase,
            'destination': self.destination
            }

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


def get_user(alexa_user_id, attr) -> User:
    return User(alexa_user_id, attr)


# def set_user(alexa_user_id, user_attr):
#     attr = {
#         'when': {
#             iso_formatted_date_today: {
#                 }
#             },
#         'last_launch_date': iso_formatted_date_today,
#         'follower_total_amount': user_attr['follower_total_amount']
#         }
#     for attribute, value in user_attr.items():
#         attr['when'][iso_formatted_date_today][attribute] = value
#     set_attr(alexa_user_id, attr)

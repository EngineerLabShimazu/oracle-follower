import boto3
import boto3.dynamodb.types as dynamodb_types

from fof_sdk import util
from fof_sdk.util import iso_formatted_date_today

dynamo = boto3.client('dynamodb')


class User:
    def __init__(self, alexa_user_id, attr):
        self.alexa_user_id: str = alexa_user_id
        self.follower_total_amount: int = attr.get('follower_total_amount', 0)
        self.last_launch_date: str = attr.get('last_launch_date', '')
        self.follower_increase: int = attr.get('follower_increase', 0)
        self.destination: str = attr.get('destination', '')
        self.possible_events: str = attr.get('possible_events', '')
        self._paid_gem: int = attr.get('paid_gem', 0)
        self._free_gem: int = attr.get('free_gem', 0)

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

    def is_first_launch_skill(self) -> bool:
        if not self.last_launch_date:
            return True
        return False

    def increase_follower(self):
        selected_event_rarity = self.possible_events[self.destination][
            'rarity']
        self.follower_increase = util.follower_table.get(
            selected_event_rarity, 5)
        self.follower_total_amount += self.follower_increase

    def set_event(self):
        self.possible_events = dict(
            (i, util.gacha()) for i in util.get_village_names())

    @property
    def contents(self):
        return self.possible_events[self.destination]['contents']

    @property
    def has_todays_oracle(self):
        if self.destination:
            return True
        return False

    def clear_destination(self):
        if self.is_first_launch_today:
            self.destination = ''

    def add_gem(self, product_reference_name):
        if product_reference_name == 'gem_1000':
            _paid_gem = 1000
            _free_gem = 300
        elif product_reference_name == 'gem_500':
            _paid_gem = 500
            _free_gem = 300
        elif product_reference_name == 'gem_300':
            _paid_gem = 300
            _free_gem = 0
        else:
            return
        self._paid_gem = _paid_gem
        self._free_gem = _free_gem
        return {'paid_gem': _paid_gem, 'free_gem': _free_gem}

    @property
    def paid_gem(self):
        return self._paid_gem

    @property
    def free_gem(self):
        return self._free_gem


def serialize_attribute(attributes):
    return dynamodb_types.TypeSerializer().serialize(attributes)


def get_user(alexa_user_id, attr) -> User:
    return User(alexa_user_id, attr)

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
        self.item_storage = attr.get('item_storage', {})

    @property
    def attr(self) -> dict:
        _attr = dict(self.__dict__)
        _attr['last_launch_date'] = iso_formatted_date_today

        # DBのcolumn nameの先頭に _ が付かないようにconvert
        _attr['paid_gem'] = self._paid_gem
        _attr['free_gem'] = self._free_gem
        _attr.pop('_paid_gem')
        _attr.pop('_free_gem')

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
            (name, util.gacha()) for name in util.get_village_names()
        )

    @property
    def content(self):
        return self.possible_events[self.destination]['content']

    @property
    def has_todays_oracle(self):
        if self.destination:
            return True
        return False

    def clear_destination(self):
        self.destination = ''

    def buy_gem(self, product_reference_name):
        if product_reference_name == 'gem_1000':
            _paid_gem = 1000
            _free_gem = 300
        elif product_reference_name == 'gem_500':
            _paid_gem = 500
            _free_gem = 100
        elif product_reference_name == 'gem_300':
            _paid_gem = 300
            _free_gem = 0
        else:
            return
        self.add_gem(_free_gem, _paid_gem)
        return {'paid_gem': _paid_gem, 'free_gem': _free_gem}

    def add_event_gem(self, event_id):
        """
        TODO こんな感じで、イベントごとの free_gem 追加 method も作りたい
        :param event_id:
        :return:
        """
        gem_events = {
            'tutorial_clear': {
                'free_gem': 100
            }
        }
        gem_event = gem_events[event_id]
        self.add_gem(gem_event['free_gem'])

    def add_gem(self, free_gem, paid_gem=0):
        self._free_gem += free_gem
        if paid_gem > 0:
            self._paid_gem += paid_gem

    @property
    def paid_gem(self):
        return self._paid_gem

    @property
    def free_gem(self):
        return self._free_gem

    def pay_gem(self, payment_amount: int) -> bool:
        # 無償ジェムで足りる場合は無償ジェムから引く
        if self.free_gem - payment_amount > 0:
            self._free_gem = self.free_gem - payment_amount
            return True

        # 無償ジェムで足りない場合は不足分を有償ジェムから引く
        if self.free_gem - payment_amount <= 0:
            unpaid = payment_amount - self.free_gem
            if self.paid_gem > unpaid:
                self._paid_gem = self.paid_gem - unpaid
                self._free_gem = 0
                return True

        return False

    def set_item(self, item_name, value):
        self.item_storage[item_name] = value

    def get_item(self, item_name, default=None):
        item = self.item_storage.get(item_name)
        if item:
            return item
        return default


def serialize_attribute(attributes):
    return dynamodb_types.TypeSerializer().serialize(attributes)


def get_user(alexa_user_id, attr) -> User:
    return User(alexa_user_id, attr)

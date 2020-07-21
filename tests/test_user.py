import datetime

from fof_sdk import user

from unittest import TestCase
from unittest.mock import patch

from fof_sdk.user import User


class TestUser(TestCase):

    def test_attr(self):
        """
        - user instance の 変数と idが違う
        - last_launch_dateが今日である
        - 全てのattributesが返却される
        """
        _user = User(alexa_user_id='dummy_id', attr={})

        self.assertEqual(_user.attr, {
            'alexa_user_id': 'dummy_id',
            'follower_total_amount': 0,
            'last_launch_date': datetime.date.today().isoformat(),
            'follower_increase': 0,
            'destination': '',
            'possible_events': '',
            'paid_gem': 0,
            'free_gem': 0,
            'item_storage': {}
        })

        self.assertNotEqual(_user.__dict__, _user.attr)

    def test_is_first_launch_today(self):
        """
        ? last_launch_date == '' is True
        ? last_launch_date is not today
        ? else
        """
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)
                     ).isoformat()
        for _user in [
            User(alexa_user_id='', attr={'last_launch_date': ''}),
            User(alexa_user_id='', attr={'last_launch_date': yesterday})
        ]:
            with self.subTest(_user.is_first_launch_today):
                self.assertTrue(_user.is_first_launch_today,
                                msg=f'{_user.last_launch_date}')

    def test_pay_gem(self):
        tests = [
            {'free_gem': 200, 'paid_gem': 0, 'payment_amount': 100, 'expected_result': True, 'remaining_free_gem': 100, 'remaining_paid_gem': 0},
            {'free_gem': 200, 'paid_gem': 200, 'payment_amount': 100, 'expected_result': True, 'remaining_free_gem': 100, 'remaining_paid_gem': 200},
            {'free_gem': 200, 'paid_gem': 200, 'payment_amount': 300, 'expected_result': True, 'remaining_free_gem': 0, 'remaining_paid_gem': 100},
            {'free_gem': 200, 'paid_gem': 0, 'payment_amount': 300, 'expected_result': False, 'remaining_free_gem': 200, 'remaining_paid_gem': 0},
            {'free_gem': 200, 'paid_gem': 200, 'payment_amount': 500, 'expected_result': False, 'remaining_free_gem': 200, 'remaining_paid_gem': 200},
            {'free_gem': 0, 'paid_gem': 0, 'payment_amount': 100, 'expected_result': False, 'remaining_free_gem': 0, 'remaining_paid_gem': 0},
            {'free_gem': 0, 'paid_gem': 200, 'payment_amount': 100, 'expected_result': True, 'remaining_free_gem': 0, 'remaining_paid_gem': 100},
            {'free_gem': 0, 'paid_gem': 200, 'payment_amount': 300, 'expected_result': False, 'remaining_free_gem': 0, 'remaining_paid_gem': 200},
        ]

        for test in tests:
            _user = User(alexa_user_id='', attr=test)
            with self.subTest(test):
                self.assertEqual(_user.pay_gem(test['payment_amount']), test['expected_result'])
                self.assertEqual(_user.free_gem, test['remaining_free_gem'])
                self.assertEqual(_user.paid_gem, test['remaining_paid_gem'])

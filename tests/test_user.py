import datetime

import user

from unittest import TestCase
from unittest.mock import patch

from user import User


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
            'follower_increase': 0
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

    @patch.object(user.random, 'choice', return_value=1)
    def test_increase_follower(self, choice):
        _user = User(alexa_user_id='', attr={'follower_total_amount': 10})
        _user.increase_follower()
        self.assertEqual(_user.follower_increase, 1)
        self.assertEqual(_user.follower_total_amount, 11)

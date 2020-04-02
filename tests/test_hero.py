from unittest import TestCase

from fof_sdk import hero
from unittest.mock import patch


class TestHero(TestCase):

    @patch.object(hero.random, 'sample', return_value=['ダミーあ', 'ダミーい'])
    def test_ask_oracle(self, sample):
        """
        文字列として正しい
        セパレーターが変更できる
        期待する中身である
        """
        self.assertEqual(hero.ask_oracle(separator='ダミー'),
                         '本日は、ダミーあダミーダミーいのどちらへ向かえばよろしいでしょうか？')

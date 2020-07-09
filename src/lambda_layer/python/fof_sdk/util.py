import os
import random
import datetime

from fof_sdk.assets.villages import villages

iso_formatted_date_today = datetime.date.today().isoformat()
"""
YYYY-mm-dd
"""

_ASSETS_URL_PREFIX = os.getenv('ASSETS_URL_PREFIX')
"""
ex.) https://bucket_name.s3-region.amazonaws.com/oracle-follower/assets
"""

follower_table = {'SS': 10,
                  'S': 9,
                  'A': 8,
                  'B': 7,
                  'C': 6,
                  'D': 5
                  }

hunt_table = {
    'A': ['MONSTER_PRECHAT'],
    'D': ['MONSTER_CARRY_RAT', 'MONSTER_LIGHT_LIZARD',
          'MONSTER_DAIFUKU_RABBIT']
}


def gacha():
    """

    :return: {'rarity': 'D', 'content': }
    """
    rarity = random.choices(['A', 'D'], weights=[5, 95])[0]
    content = random.choice(hunt(rarity))
    return {'rarity': rarity, 'content': content}


def hunt(rarity):
    return hunt_table[rarity]


def valid_destination(destination_intent) -> str:
    """
    :param destination_intent:
    :return: village.actual_name
    - ホワイトタウン
    - ホワイトxxx
    - xxxタウン
    - ホワイト タウン
    - ホワイト xxx
    - xxx タウン
    """
    for i in villages.values():
        for words in i['variation'].values():
            for word in words:
                if word in destination_intent:
                    return i['actual_name']
    return ''


def get_village_names():
    return [i['actual_name'] for i in villages.values()]


def get_image(image_key: str, extension: str = '.png') -> str:
    """
    :param image_key: 関数内で小文字に変換します。ex) hero/hero_anticipation.jpg
    :param extension:
    :return: url ex.) https://bucket_name.s3-region.amazonaws.com/oracle-follower/assets/images/hero/hero_anticipation.jpg
    """
    return f'{_ASSETS_URL_PREFIX}/images/{image_key.lower()}{extension}'

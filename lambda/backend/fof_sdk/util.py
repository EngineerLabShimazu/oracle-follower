import random
import datetime

from fof_sdk.assets.villages import villages

iso_formatted_date_today = datetime.date.today().isoformat()
"""
YYYY-mm-dd
"""

follower_table = {'SS': 10,
                  'S': 9,
                  'A': 8,
                  'B': 7,
                  'C': 6,
                  'D': 5
                  }

hunt_table = {
    'SS': ['堕天使'],
    'S': ['青龍', '白虎', '朱雀', '玄武'],
    'A': ['ヴァンパイア'],
    'B': ['ゴーレム', 'オーガ'],
    'C': ['ゴブリン', 'イエティ'],
    'D': ['コウモリ', 'スライム']
}


def gacha():
    rarity = random.choices(['SS', 'S', 'A', 'B', 'C', 'D'],
                            weights=[0.1, 0.5, 5, 20, 30, 44.4])[0]
    contents = random.choice(hunt(rarity))
    return {'rarity': rarity, 'contents': contents}


def hunt(rarity):
    return hunt_table[rarity]


def is_valid_destination(destination):
    if destination in villages:
        return True
    return False

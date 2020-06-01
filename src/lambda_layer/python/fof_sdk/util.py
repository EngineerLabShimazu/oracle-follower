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


def is_support_display(handler_input):
    try:
        if hasattr(
                handler_input.request_envelope.context.system.device.supported_interfaces,
                'display'):
            return (
                    handler_input.request_envelope.context.system.device.
                    supported_interfaces.display is not None)
    except:
        return False

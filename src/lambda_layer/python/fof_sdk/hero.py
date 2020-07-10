import random
from typing import List

from fof_sdk import util


def get_appreciate_message_legacy() -> str:
    messages = ["見守ってくださって",
                "お気にかけてくださって",
                "健やかに暮らさせていただき",
                "祈りを受け入れてくださり"]
    return random.choice(messages)


def get_appreciate_message() -> str:
    messages = ["HERO_APPRECIATE_1",
                "HERO_APPRECIATE_2",
                "HERO_APPRECIATE_3",
                "HERO_APPRECIATE_4"]
    return random.choice(messages)


def message_legacy():
    return f"こんにちは神様。本日も{get_appreciate_message()}、ありがとうございます。"


def message():
    return {
        'text': 'HERO_MESSAGE',
        'kwargs': {
            'appreciate': get_appreciate_message()
            }
        }


def action_report_lecacy(destination, monster):
    return f"昨日は{destination}へ行き、{monster}を討伐してまいりました！"


def action_report(destination, monster: str):
    return {
        'original_texts': {
            'text': 'HERO_ACTION_REPORT',
            'kwargs': {
                'destination': destination,
                'monster': monster
            }
        },
        'bg_image_url': util.get_image(f'reports/{monster.lower()}')
    }


def increase_follower_legacy(follower_increase, total_follower):
    return f"その結果、神様を信仰させていただきたいと申す者共が新たに{follower_increase}人増えました。現在の合計は{total_follower}人です。"


def increase_follower(follower_increase):
    return {
        'text': 'HERO_INCREASE_FOLLOWER',
        'kwargs': {
            'follower_increase': follower_increase
            }
        }


def total_followers(total_follower):
    return {
        'text': 'HERO_TOTAL_FOLLOWERS',
        'kwargs': {
            'total_follower': total_follower
            }
        }


def ask_oracle_legacy(destinations, separator='と'):
    destinations_text = separator.join(destinations)
    ask_oracle_text = f"本日は、{destinations_text}のどちらへ向かえばよろしいでしょうか？"
    return ask_oracle_text


def ask_oracle(destinations: List[str]):
    return {
        'text': 'HERO_ASK_ORACLE',
        'kwargs': {
            'destination_a': destinations[0],
            'destination_b': destinations[1]
            }
        }


def repeat_oracle_legacy(destination):
    return f'{destination}へ行くのですね！ありがとうございます！また明日、結果を報告します！'


def repeat_oracle(destination):
    return {
        'text': 'HERO_REPEAT_ORACLE',
        'kwargs': {
            'destination': destination
            }
        }


def pardon():
    return {
        'text': 'HERO_PARDON'
        }

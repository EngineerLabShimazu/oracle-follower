import random
from fof_sdk.assets.villages import villages


def get_appreciate_message() -> str:
    messages = ["見守ってくださって",
                "お気にかけてくださって",
                "健やかに暮らさせていただき",
                "祈りを受け入れてくださり"]
    return random.choice(messages)


def message():
    return f"こんにちは神様。本日も{get_appreciate_message()}、ありがとうございます。"


def increase_follower(follower_increase, total_follower):
    return f"昨日、信者の数が{follower_increase}人増えました。現在の合計は{total_follower}人です。"


def ask_oracle(separator='と'):
    destinations = separator.join(random.sample(villages, 2))
    ask_oracle_text = f"本日は、{destinations}のどちらへ向かえばよろしいでしょうか？"
    return ask_oracle_text


def repeat_oracle(destination):
    return f'{destination}へ行くのですね！ありがとうございます！'

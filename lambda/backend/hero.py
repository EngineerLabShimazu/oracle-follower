import random


def get_appreciate_message() -> str:
    messages = ["見守ってくださって",
                "お気にかけてくださって",
                "健やかに暮らさせていただき",
                "祈りを受け入れてくださり"]
    return random.choice(messages)


def message():
    return f"こんにちは神様。本日も{get_appreciate_message()}、ありがとうございます。"

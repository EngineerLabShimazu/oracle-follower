import random


def get_appreciate_message() -> str:
    messages = ["見守ってくださって",
                "お気にかけてくださって",
                "健やかに暮らさせていただき",
                "祈りを受け入れてくださり"]
    return random.choice(messages)


def message():
    return f"こんにちは神様。本日も{get_appreciate_message()}、ありがとうございます。"


def action_report(destination, monster):
    return f"昨日は{destination}へ行き、{monster}を討伐してまいりました！"


def increase_follower(follower_increase, total_follower):
    return f"その結果、神様を信仰させていただきたいと申す者共が新たに{follower_increase}人増えました。現在の合計は{total_follower}人です。"


def ask_oracle(destinations, separator='と'):
    destinations_text = separator.join(destinations)
    ask_oracle_text = f"本日は、{destinations_text}のどちらへ向かえばよろしいでしょうか？"
    return ask_oracle_text


def repeat_oracle(destination):
    return f'{destination}へ行くのですね！ありがとうございます！また明日、結果を報告します！'
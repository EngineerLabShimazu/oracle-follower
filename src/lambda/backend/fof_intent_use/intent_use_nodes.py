from fof_sdk import hero
from fof_sdk import util
from fof_sdk.user import User


def launch(user: User, intent):
    if user.has_todays_oracle:
        return {
            'type': 'use',
            'node': 'use_ticket',
            'original_texts': [
                {
                    'text': 'CONFIRM_CHRONUS_TICKET'
                }
            ]
        }
    return {
        'type': 'oracle',
        'original_texts': [
            {
                'text': 'PLEASE_ORACLE'
            },
            hero.message(),
            hero.ask_oracle(util.get_destinations_choice()),
        ]
    }


def use_ticket(user: User, intent):
    if intent == 'No':
        return {
            'type': 'end',
            'set_should_end_session': True,
            'original_texts': [
                {
                    'text': 'TICKET_NOT_USED'
                }
            ]
        }

    original_texts = []
    # 昨日の活動報告を聞く
    action_parts = hero.action_report(user.destination, user.content)

    # 信者を獲得
    user.increase_follower()
    original_texts.append(hero.increase_follower(
        user.follower_increase))
    original_texts.append(hero.total_followers(
        user.follower_total_amount))

    # 昨日のお告げによって目的地へは行って帰ってきたのでクリア
    user.clear_destination()

    # 今日の目的地ガチャ
    user.set_event()
    return {
        'type': 'oracle',
        'user_attr': user.attr,
        'original_texts': [
            {
                'text': 'AUDIO_TIME_PASS'
            },
            {
                'text': 'EARTH_TIME_PASSED'
            },
            hero.message(),
            action_parts['original_texts'],
            hero.ask_oracle(util.get_destinations_choice()),
        ]
    }

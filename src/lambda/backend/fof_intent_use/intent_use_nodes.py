import use_util
from fof_sdk import hero
from fof_sdk import util
from fof_sdk.user import User


def re_ask():
    return {
        'type': 'use',
        'node': 'use_ticket',
        'original_texts': [
            {
                'text': 'CONFIRM_CHRONUS_TICKET'
            }
        ],
        'set_should_end_session': False,
    }


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
    if intent == 'AMAZON.NoIntent':
        return {
            'type': 'end',
            'set_should_end_session': True,
            'original_texts': [
                {
                    'text': 'TICKET_NOT_USED'
                }
            ]
        }

    if not use_util.has_chronus_ticket(user):
        return {
            'type': 'ganesha',
            'node': 'launch',
            'original_texts': [
                {
                    'text': 'RECOMMEND_CHRONUS_TICKET'
                }
            ]
        }

    use_util.use_ticket(user)

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
                'text': 'EARTH_TIME_PASSED'
            },
            {
                'text': 'AUDIO_TIME_PASS'
            },
            hero.message(),
            action_parts['original_texts'],
            hero.ask_oracle(util.get_destinations_choice()),
        ],
        'image_url': action_parts['image_url'],
        'bg_image_url': action_parts['bg_image_url']
    }

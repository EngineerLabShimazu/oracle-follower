from fof_sdk import hero
from fof_sdk import util


def re_ask():
    return {
        'original_texts': [
            {
                'text': 'RECOMMEND_CHRONUS_TICKET',
            }
        ],
        'set_should_end_session': False,
        'type': 'launch',
        'node': 'buy_ticket'
    }


def ganesha():
    return {
        'original_texts': [
            {
                'text': 'WELCOME_TO_GANESHA_SHOP',
            },
            {
                'text': 'SALES_GATCHA'
            },
            {
                'text': 'RECOMMEND_TEN'
            }
        ],
        'turn_times': 10,
        'type': 'ganesha',
        'node': 'welcome',
        'image_url': util.get_image('gods/ganesha'),
        'bg_image_url': util.get_image('bg/ganesha-shop',
                                       extension='.jpg'),
        'set_should_end_session': False
    }


def end():
    return {
        'original_texts': [
            {
                'text': 'APPRECIATE_ON_STOP',
                'kwargs': {
                    'appreciate': hero.get_appreciate_message()
                }
            }
        ],
        'type': 'end',
        'set_should_end_session': True
    }

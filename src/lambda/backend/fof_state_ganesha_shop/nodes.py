def launch():
    return {
        'original_texts': [
            {
                'text': 'WELCOME_TO_GANESHA_SHOP',
            },
            {
                'text': 'SALES_GATCHA'
            }
        ],
        'turn_times': 10
    }


def recommend():
    return {
        'original_texts': [
            {
                'text': 'RECOMMEND_GATCHA',
            }
        ],
        'turn_times': 1
    }


def gatcha(turn_times):
    turn_times_text = '一回' if turn_times == 1 else '十連'
    return {
        'original_texts': [
            {
                'text': 'GANESHA_THANKS',
            },
            {
                'text': 'GATCHA',
            },
            {
                'text': 'GATCHA_AGAIN',
                'kwargs': {
                    'turn_times_text': turn_times_text
                }
            }
        ],
        'turn_times': turn_times
    }


def end():
    return {
        'original_texts': [
            {
                'text': 'END_SHOP',
            }
        ],
        'type': 'launch',
        'set_should_end_session': True
    }

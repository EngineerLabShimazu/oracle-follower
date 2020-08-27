import consts

def launch():
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
        'turn_times': 10
    }


def recommend_ten():
    return {
        'original_texts': [
            {
                'text': 'RECOMMEND_TEN'
            }
        ],
        'turn_times': 10
    }


def recommend_gatcha():
    return {
        'original_texts': [
            {
                'text': 'RECOMMEND_GATCHA',
            }
        ],
        'turn_times': 1
    }


def recommend_gem(turn_times, not_enough_gem):
    if not_enough_gem <= 300:
        gem_pack_grade = '小'
        product_name = 'gem_300'
    elif 300 < not_enough_gem <= 600:
        gem_pack_grade = '中'
        product_name = 'gem_500'
    else:
        gem_pack_grade = '大'
        product_name = 'gem_1000'
    return {
        'original_texts': [
            {
                'text': 'RECOMMEND_GEM',
                'kwargs': {
                    'not_enough_gem': not_enough_gem,
                    'gem_pack_grade': gem_pack_grade
                }
            }
        ],
        'turn_times': turn_times,
        'product_name': product_name,
        'not_enough_gem': not_enough_gem
    }


def gatcha(turn_times, items, user):
    turn_times_text = '' if turn_times == 1 else '十連'
    gatcha_items = {
        'chronus_ticket_1': {
            'sound': 'GATCHA_SOUND_1',
            'item_name': 'CHRONUS_TICKET_1',
            'ticket_amount': 1
        },
        'chronus_ticket_3': {
            'sound': 'GATCHA_SOUND_3',
            'item_name': 'CHRONUS_TICKET_3',
            'ticket_amount': 3
        },
        'chronus_ticket_10': {
            'sound': 'GATCHA_SOUND_10',
            'item_name': 'CHRONUS_TICKET_10',
            'ticket_amount': 10
        },
    }

    original_texts = [
        {
            'text': 'GANESHA_THANKS',
        }]

    total_ticket_amount = 0
    for item in items:
        original_texts.append({
            'text': gatcha_items[item]['sound'],
        })
        original_texts.append({
            'text': gatcha_items[item]['item_name'],
        })
        original_texts.append({
            'text': 'BREAK_TIME_1S',
        })
        total_ticket_amount += gatcha_items[item]['ticket_amount']

    original_texts.append({
        'text': 'TOTAL_TICKET_AMOUNT',
        'kwargs': {
            'total_ticket_amount': total_ticket_amount
        }
    })

    remaining_free_gem = user.free_gem
    remaining_paid_gem = user.paid_gem

    original_texts.append({
        'text': 'REMAINGING_GEM',
        'kwargs': {
            'remaining_free_gem': remaining_free_gem,
            'remaining_paid_gem': remaining_paid_gem
        }
    })

    original_texts.append({
        'text': 'GATCHA_AGAIN',
        'kwargs': {
            'turn_times_text': turn_times_text
        }
    })

    return {'original_texts': original_texts,
            'turn_times': turn_times,
            'total_ticket_amount': total_ticket_amount
            }


def result(total_ticket_amount, turn_times, user):
    original_texts = []
    original_texts.append({
        'text': 'TOTAL_TICKET_AMOUNT',
        'kwargs': {
            'total_ticket_amount': total_ticket_amount
        }
    })

    remaining_free_gem = user.free_gem
    remaining_paid_gem = user.paid_gem

    original_texts.append({
        'text': 'REMAINGING_GEM',
        'kwargs': {
            'remaining_free_gem': remaining_free_gem,
            'remaining_paid_gem': remaining_paid_gem
        }
    })

    turn_times_text = '' if turn_times == 1 else '十連'
    original_texts.append({
        'text': 'GATCHA_AGAIN',
        'kwargs': {
            'turn_times_text': turn_times_text
        }
    })

    return {
        'original_texts': original_texts,
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

def launch():
    return {
        'original_texts': [
            {
                'text': 'TUTORIAL_LAUNCH',
            }
        ],
        'state': 'tutorial',
        'node': 'salvation'
    }


def salvation(intent):
    if intent == 'DestinationIntent':
        return {
            'original_texts': [
                {
                    'text': 'TUTORIAL_SALVATION',
                }
            ],
            'state': 'tutorial',
            'node': 'send_out'
        }
    return {
        'original_texts': [
            {
                'text': 'TUTORIAL_SALVATION_ASK',
            }
        ],
        'state': 'tutorial',
        'node': 'salvation'
    }


def salvation_ask():
    return {
        'original_texts': [
            {
                'text': 'TUTORIAL_SALVATION_ASK'
            }
        ]
    }


def send_out(intent, destination):
    if intent == 'DestinationIntent':
        return {
            'original_texts': [
                {
                    'text': 'TUTORIAL_SEND_OUT',
                    'kwargs': {
                        'destination': destination
                    }
                }
            ],
            'end': True
        }
    return {
        'original_texts': [
            {
                'text': 'TUTORIAL_SEND_OUT_ASK'
            }
        ],
        'state': 'tutorial',
        'node': 'salvation'
    }

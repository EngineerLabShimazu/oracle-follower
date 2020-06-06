def launch():
    return {
        'original_text': {
            'text': 'TUTORIAL_LAUNCH'
            },
        'node': 'salvation'
        }


def salvation():
    return {
        'original_text': {
            'text': 'TUTORIAL_SALVATION'
            },
        'node': 'send_out'
        }


def send_out(destination):
    return {
        'original_text': {
            'text': 'TUTORIAL_SEND_OUT',
            'kwargs': {
                'destination': destination
                }
            },
        'end': True
        }

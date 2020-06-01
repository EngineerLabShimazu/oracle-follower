def main():
    action = {
        'type': 'tutorial',
        'set_should_end_session': False
        }
    response_text = """
    """
    action['response_text'] = ''.join(response_text)
    return action


def lambda_handler(event, context):
    response = main()
    return response

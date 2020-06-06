from tutorial import text_map


def translate_text(text_key: str, **kwargs) -> str:
    """
    :param text_key: TUTORIAL_SEND_OUT
    :param kwargs: ex.) ** {'destination': 'マゼンタコート'}
    """
    base_text: str = text_map.get(text_key, '')
    return base_text.format(**kwargs)


def lambda_handler(event, context):
    response_text = event.get('original_text')
    text_key = response_text.get('text')
    parameters = response_text.get('kwargs', {})
    response_text = translate_text(text_key, **parameters)
    if not response_text:
        return text_key
    return response_text

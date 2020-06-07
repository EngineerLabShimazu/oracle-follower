import tutorial
import hero

text_maps = [
    tutorial.text_map,
    hero.text_map
    ]


def translate_text(text_key: str, **kwargs) -> str:
    """
    :param text_key: TUTORIAL_SEND_OUT
    :param kwargs: ex.) ** {'destination': 'マゼンタコート'}
    """
    for text_map in text_maps:
        base_text: str = text_map.get(text_key, '')
        return base_text.format(**kwargs)
    return ''


def main(original_texts) -> str:
    response_texts = []
    for original_text in original_texts:
        text_key = original_text.get('text')
        parameters = original_text.get('kwargs', {})
        translated_text = translate_text(text_key, **parameters)
        response_texts.append(translated_text)
    return ''.join(response_texts)


def lambda_handler(event, context):
    original_texts = event.get('original_texts')
    response_text = main(original_texts)
    return response_text

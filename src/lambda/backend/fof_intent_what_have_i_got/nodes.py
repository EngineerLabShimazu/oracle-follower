def re_ask(node):
    if node == 'ask_ganesha':
        return {
            'type': 'what_have_i_got',
            'set_should_end_session': False,
            'original_texts': [
                {
                    'text': 'ASK_GANESHA',
                }
            ]
        }
    elif node == 'ask_gem_pack':
        return {
            'type': 'what_have_i_got',
            'set_should_end_session': False,
            'original_texts': [
                {
                    'text': 'ASK_GEM_PACK',
                }
            ]
        }

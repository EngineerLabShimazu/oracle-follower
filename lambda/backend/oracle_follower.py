import json

import hero
import user


def main(info):
    loaded_info = json.loads(info)
    user.set_user(loaded_info['user_id'], {})
    response_text = hero.message()
    response = {"response_text": response_text}
    return json.dumps(response)

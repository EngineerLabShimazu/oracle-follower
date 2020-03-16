import json

import hero
import user


def main(info):
    loaded_info = json.loads(info)

    _user = user.get_user(alexa_user_id=loaded_info['alexa_user_id'])
    if _user.is_first_launch_today:
        _user.increase_follower()

    response_text = hero.message()
    response = {"response_text": response_text}
    return json.dumps(response)

import json

import hero
import user


def main(info):
    loaded_info = json.loads(info)

    _user = user.get_user(alexa_user_id=loaded_info['alexa_user_id'])
    response_text = [hero.message()]

    if _user.is_first_launch_today:
        _user.increase_follower()
        response_text.append(hero.increase_follower(_user.follower_increase,
                                                    _user.follower_total_amount))

    response = {"response_text": "。".join(response_text)}
    return json.dumps(response)

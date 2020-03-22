import json

import hero
import user
from dynamo_ctl import DynamoCtl


def main(info):
    loaded_info = json.loads(info)

    alexa_user_id = loaded_info['alexa_user_id']
    with DynamoCtl(alexa_user_id) as dynamo_ctl:
        _user = user.get_user(alexa_user_id, dynamo_ctl.attr)
        response_text = [hero.message()]

        if _user.is_first_launch_today:
            _user.increase_follower()
            response_text.append(hero.increase_follower(
                _user.follower_increase, _user.follower_total_amount))

        response = {"response_text": "".join(response_text)}
        dynamo_ctl.attr = _user.attr

    return json.dumps(response)

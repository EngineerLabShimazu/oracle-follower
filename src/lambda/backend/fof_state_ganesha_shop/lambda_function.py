import random
from gatcha_items import gatcha_items


def lottery():
    item_name_list = []
    weight_list = []
    for k, item in gatcha_items.items():
        item_name_list.append(item['name'])
        weight_list.append(item['ratio'])

    item = random.choices(item_name_list, weight_list)[0]
    return item


def gatcha(turn_times):
    if turn_times == 1:
        lottery()
    if turn_times == 10:
        pass


def main(alexa_user_id, turn_times):
    action = {'type': 'ganesha',
              "original_texts": [
                  {
                      'text': 'WELCOME_TO_GANESHA_SHOP'
                  },
                  {
                      'text': 'SALES_GATCHA'
                  }
              ]
              }

    return action


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    turn_times = event['turn_times']
    response = main(alexa_user_id, turn_times)
    return response

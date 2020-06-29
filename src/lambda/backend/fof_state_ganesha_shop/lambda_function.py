def main():
    action = {'type': 'end',
              "original_texts": [
                  {
                      'text': 'WELCOME_TO_GANESHA_SHOP'
                  }
              ]
              }
    return action


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    response = main(alexa_user_id)
    return response

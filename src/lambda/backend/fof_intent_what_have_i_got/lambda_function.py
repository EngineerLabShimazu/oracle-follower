from fof_sdk.user import User


def main():
    return 'hello from what-have-i-got main!'


def lambda_handler(event, context):
    user = User(event['alexa_user_id'], event['dynamo_attr'])
    response = main(user)
    return response

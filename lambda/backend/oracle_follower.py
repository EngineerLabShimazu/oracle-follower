import json

import hero


def main():
    response_text = hero.message()
    response = {"response_text": response_text}
    return json.dumps(response)

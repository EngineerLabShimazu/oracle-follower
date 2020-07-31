def lambda_handler(event, context):
    node = event.get('node')
    action_type = event.get('type')
    state = event.get('state')
    if not (node and action_type and state):
        return ''

    if action_type != state:
        # stateが変わったなら、nodeをクリア
        return ''

    return node

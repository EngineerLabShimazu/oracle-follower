from nodes import node_map


def main(node_key):
    action = {
        'type': 'tutorial',
        'set_should_end_session': False
        }
    node = node_map.get(node_key)
    action['response_text'] = ''.join(node['text'])
    action['node'] = node.get('next_node', '')

    if node.get('end'):
        action['set_should_end_session'] = True
    return action


def lambda_handler(event, context):
    node_key = event.get('node', 'launch')
    action = main(node_key)
    return action

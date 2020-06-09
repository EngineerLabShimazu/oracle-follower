def get_env_type(handler_input):
    if 'prd' in handler_input.context.invoked_function_arn:
        return 'prd'
    return 'stg'


def is_support_display(handler_input):
    try:
        if hasattr(
                handler_input.request_envelope.context.system.device.supported_interfaces,
                'display'):
            return (
                    handler_input.request_envelope.context.system.device.
                    supported_interfaces.display is not None)
    except:
        return False

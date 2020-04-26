def get_env_type(handler_input):
    if 'prd' in handler_input.context.invoked_function_arn:
        return 'prd'
    return 'stg'

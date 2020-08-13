def get_env(context) -> str:
    """
    fof_{function_name}_{env} の {env} で、対象がprdかstgか判断する
    :return: 'prd' or 'stg'
    """
    env_str_count = 3
    fof_name_env = context.function_name
    if len(fof_name_env) < env_str_count:
        return 'stg'
    return 'prd' if 'prd' in fof_name_env[-env_str_count:] else 'stg'

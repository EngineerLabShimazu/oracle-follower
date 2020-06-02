import os
import json
import time
import boto3


def get_sfn_arn(env_type):
    if env_type == 'prd':
        return os.getenv('BACKEND_SFN_ARN_PRD')
    return os.getenv('BACKEND_SFN_ARN_STG')


def execute(start_execution_input):
    client = boto3.client('stepfunctions')
    fof_sfn_arn = get_sfn_arn(start_execution_input.get('env_type'))
    start_res = client.start_execution(
        stateMachineArn=fof_sfn_arn, input=json.dumps(start_execution_input))

    for i in [1.0, 2.0, 3.0]:
        des_res = client.describe_execution(
            executionArn=start_res['executionArn'])
        if 'output' in des_res:
            break
        else:
            time.sleep(i)
            print('describe_execution response has not exists "output" key. '
                  'retry...')
            continue
    output = des_res["output"]
    print(f'output: {output}')
    return json.loads(output)

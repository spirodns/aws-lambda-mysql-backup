import boto3

def get_aws_parameter_store_value(parameter_store_key, region):
    # Function for get_parameters
    def get_parameters(param_key):
        ssm = boto3.client('ssm', region_name=region)
        response = ssm.get_parameters(
            Names=[
                param_key,
            ],
            WithDecryption=True
        )
        return response['Parameters'][0]['Value']
    # get parameter value
    param_value = get_parameters(parameter_store_key)
    parameter_store_value_string=str(param_value)
    return parameter_store_value_string




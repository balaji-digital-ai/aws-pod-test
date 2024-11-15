import boto3
import json
import os

def invoke_lambda(function_name, region, assume_role=None):
    print("Starting Lambda invocation...")
    print(f"Function Name: {function_name}")
    print(f"Region: {region}")
    print(f"Assume Role: {'Provided' if assume_role else 'Not Provided'}")

    if assume_role:
        print("Assume role passed, using assume role logic.")
        sts_client = boto3.client('sts', region_name=region)
        print("STS client created successfully.")

        assumed_role = sts_client.assume_role(
            RoleArn=assume_role,
            RoleSessionName='LambdaInvokeSession'
        )
        print("Assume role call successful.")
        credentials = assumed_role['Credentials']

        print("Temporary credentials obtained:")
        print(f"Access Key ID: {credentials['AccessKeyId']}")
        print(f"Session Token (truncated): {credentials['SessionToken'][:20]}...")

        lambda_client = boto3.client(
            'lambda',
            region_name=region,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        print("Lambda client created with assumed role credentials.")
    else:
        print("Assume role not passed, using pod role.")
        lambda_client = boto3.client('lambda', region_name=region)
        print("Lambda client created with pod role.")

    # Payload to send to Lambda
    payload = {
        'key': 'value'
    }
    print("Payload prepared for Lambda invocation:")
    print(json.dumps(payload, indent=2))

    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  # or 'Event' for async
            Payload=json.dumps(payload)
        )
        print("Lambda invocation successful.")
    except Exception as e:
        print(f"Error during Lambda invocation: {str(e)}")
        raise

    # Print the status code and response payload
    status_code = response['StatusCode']
    response_payload = response['Payload'].read()

    print(f"Response Code: {status_code}")
    print("Response Payload:")
    print(response_payload)

    return response_payload

if __name__ == "__main__":
    print("Starting script execution...")
    function_name = os.getenv('FUNCTION_NAME')
    region = os.getenv('REGION')
    assume_role = os.getenv('ASSUME_ROLE')  # Pass the role ARN or leave blank if not using

    if not function_name or not region:
        raise ValueError("FUNCTION_NAME and REGION environment variables must be set.")
    
    print("Environment variables validated.")
    print(f"FUNCTION_NAME: {function_name}")
    print(f"REGION: {region}")
    if assume_role:
        print(f"ASSUME_ROLE provided: {assume_role[:20]}... (truncated for display)")

    result = invoke_lambda(function_name, region, assume_role)
    print("Script execution completed.")

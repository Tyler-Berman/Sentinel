# Create a Lambda Function from Python
# Create an IAM Role for the Lambda Function with necessary permissions
# Attach the IAM Role to the Lambda Function
import time
import boto3
import os
from dotenv import load_dotenv
import json
load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY') 
SNS_TOPIC_ARN = os.getenv('TOPIC_ARN')
Trust_Policy = {"Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}
IAM = boto3.client('iam',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-2')

LAMBDA = boto3.client('lambda',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-2'
)
LAMBDA_ROLE_NAME = 'S3SecurityAuditLambdaRole'
role_response = IAM.create_role(
    RoleName=LAMBDA_ROLE_NAME,
    AssumeRolePolicyDocument=json.dumps(Trust_Policy)
)
role_arn = role_response['Role']['Arn']
policies = [
    'arn:aws:iam::aws:policy/AmazonS3FullAccess',
    'arn:aws:iam::aws:policy/AmazonSNSFullAccess',
    'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
]

for policy_arn in policies:
    print(f"Attaching policy: {policy_arn}")
    IAM.attach_role_policy(RoleName=LAMBDA_ROLE_NAME, PolicyArn=policy_arn)


time.sleep(10)  
with open('LAMBDA_COPY_FOR_AUDIT_SNS.ZIP.zip', 'rb') as f:
    zipped_code = f.read()
LAMBDA_FUNCTION_NAME = 'S3SecurityAuditLambda'
LAMBDA.create_function(
    FunctionName=LAMBDA_FUNCTION_NAME,
    Runtime='python3.8',
    Role=role_arn, 
    Handler='LAMBDA_COPY_FOR_AUDIT_SNS.lambda_handler',
    Code={'ZipFile': zipped_code},
    Description='Sentinel Phase 6: Automated S3 Remediation',
    Timeout=15, 
    Environment={
        'Variables': {
            'TOPIC_ARN': os.getenv('TOPIC_ARN')
        }
    })                  

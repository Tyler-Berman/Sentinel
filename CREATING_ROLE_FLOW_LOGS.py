from dotenv import load_dotenv
import json
import boto3
import os
load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY') 

# Create Trust Policy for VPC Flow Logs
flow_log_trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "vpc-flow-logs.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
iam = boto3.client('iam', region_name='us-east-2')
# Create inline policy for flow logs
flow_log_permission_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}

ROLE_NAME = 'VPCFlowLogsRole'

try:
    print(f"Sentinel Phase 8: Creating IAM Role '{ROLE_NAME}'...")
    # Create role, pass in role_name, attach trust policy
    role_response = iam.create_role(
        RoleName=ROLE_NAME,
        AssumeRolePolicyDocument=json.dumps(flow_log_trust_policy)
    )
    # Pass through role_response, retreive ARN from created role
    role_arn = role_response['Role']['Arn']
    print(f"Role Created. ARN: {role_arn}")
    # Add permission policy, use put instead of attach for inline policy
    iam.put_role_policy(
        RoleName=ROLE_NAME,
        PolicyName='VPCFlowLogDeliveryPolicy',
        PolicyDocument=json.dumps(flow_log_permission_policy)
    )
    print("Permissions Attached.")
# add a try/except to handle errors
except iam.exceptions.EntityAlreadyExistsException:
    role_response = iam.get_role(RoleName=ROLE_NAME)
    role_arn = role_response['Role']['Arn']
    print(f"Role already exists. ARN: {role_arn}")

except Exception as e:
    print(f"ERROR: {e}")
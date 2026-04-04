# Create IAM Role for Bedrock that includes all relevant policies

import boto3
import os
from dotenv import load_dotenv
import json
load_dotenv()
account_id = os.getenv('MY_ACCOUNT_ID')
iam = boto3.client('iam',
                   region_name='us-east-2')
bucket_name = os.getenv('bucket_name')
trust_policy = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "bedrock.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
role_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "BedrockModelInvocation",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:ListFoundationModels",
                "bedrock:GetFoundationModel"
            ],
            "Resource": "*"
        },
        {
            "Sid": "S3ReadWriteAccess",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                "arn:aws:s3:::ai-sentinel-security-reports-2026",
                "arn:aws:s3:::ai-sentinel-security-reports-2026/*"
            ]
        },
        {
            "Sid": "BedrockServiceRolePassRole",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": "arn:aws:iam::{account_id}:role/Bedrock_Role",
            "Condition": {
                "StringEquals": {
                    "iam:PassedToService": "bedrock.amazonaws.com"
                }
            }
        }
    ]
}
role_name = 'Bedrock_Role'
try:
    role_response = iam.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=json.dumps(trust_policy))
    
    print(f"Created IAM role '{role_name}'")
    role_arn = role_response['Role']['Arn']
    print(f"Role Created. ARN: {role_arn}")
    
    iam.put_role_policy(
        RoleName=role_name,
        PolicyName='BedrockPolicy',
        PolicyDocument=json.dumps(role_policy)
    )
    print("Permissions Attached.")
except iam.exceptions.EntityAlreadyExistsException:
    role_response = iam.get_role(RoleName=role_name)
    role_arn = role_response['Role']['Arn']
    print(f"Role already exists. ARN: {role_arn}")

except Exception as e:
    print(f"ERROR: {e}")

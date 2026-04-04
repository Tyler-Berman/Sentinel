import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

iam = boto3.client('iam')
role_name = 'Sentinel_Lambda_Execution_Role'

SNS_ARN = os.getenv('TOPIC_ARN_2')

sentinel_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:ListBucket"],
            "Resource": [
                "arn:aws:s3:::ai-sentinel-security-reports-2026",
                "arn:aws:s3:::ai-sentinel-security-reports-2026/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": SNS_ARN 
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}

def attach_sentinel_permissions():

    if not SNS_ARN:
        print("Error: TOPIC_ARN_2 not found in .env file!")
        return

    print(f"Attaching Sentinel permissions to {role_name}...")
    try:
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName='Sentinel_Lambda_Permissions',
            PolicyDocument=json.dumps(sentinel_policy)
        )
        print("Lambda Role is now fully powered!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    attach_sentinel_permissions()
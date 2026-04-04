import boto3
import json
import os
from dotenv import load_dotenv
load_dotenv()

iam = boto3.client('iam')
role_name = 'Sentinel_Lambda_Execution_Role'

def create_sentinel_role():
    trust_relationship = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }

    print(f"Creating IAM Role: {role_name}...")
    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_relationship)
        )
        print(f"Role Created! ARN: {response['Role']['Arn']}")
    except iam.exceptions.EntityAlreadyExistsException:
        print("Role already exists, we are good to go.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_sentinel_role()
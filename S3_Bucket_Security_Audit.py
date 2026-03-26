# Connect to S3 console
# Check public access settings for the S3 bucket
# Print out the results

import boto3
import os   
from dotenv import load_dotenv
load_dotenv()
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

s3 = boto3.client('s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-2'
)
BUCKET_NAME = 'sentinel-test-bucket-2026'
security_check = s3.get_public_access_block(Bucket=BUCKET_NAME)

Public_Access = security_check['PublicAccessBlockConfiguration']

Public_ACL_Access = Public_Access['BlockPublicAcls']
if Public_ACL_Access == True:
    print("Public ACLs are blocked for this bucket.")
else:
    print("This bucket allows public ACLs.")

Public_Policy = Public_Access['BlockPublicPolicy']
if Public_Policy == True:
    print("Public bucket policies are blocked for this bucket.")
else:
    print("This bucket allows public bucket policies.")
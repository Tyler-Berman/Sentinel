# Connect to S3 console
# Check public access settings 
# Remediate any unwanted access settings 
# Print out the results

import boto3
import os
from dotenv import load_dotenv
load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client('s3', 
    aws_access_key_id=aws_access_key_id, 
    aws_secret_access_key=aws_secret_access_key, 
    region_name='us-east-2'
)  

BUCKET_NAME = 'sentinel-test-bucket-2026'
SECURITY_CHECK = s3.get_public_access_block(Bucket=BUCKET_NAME)

PUBLIC_ACCESS = SECURITY_CHECK['PublicAccessBlockConfiguration']

PUBLIC_POLICY = PUBLIC_ACCESS['BlockPublicPolicy']
PUBLIC_ACLS = PUBLIC_ACCESS['BlockPublicAcls']

if PUBLIC_POLICY == True and PUBLIC_ACLS == True:
    print(f"Public access settings for bucket '{BUCKET_NAME}' are compliant.")
else: 
    s3.put_public_access_block(
        Bucket=BUCKET_NAME,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
    )
    print(f"Public access settings for bucket '{BUCKET_NAME}' have been remediated to be compliant.")



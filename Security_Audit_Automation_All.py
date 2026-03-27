# Automate security remediation for all S3 buckets public access settings using Boto3 in Python.
# Make sure the code doesn't fail if a bucket doesn't have a public access block configuration, and instead remediates it to be compliant.

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

ALL_BUCKETS = s3.list_buckets()
for bucket in ALL_BUCKETS['Buckets']:
    BUCKET_NAME = bucket['Name']
    try:
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
    
    except s3.exceptions.NoSuchPublicAccessBlockConfiguration:
            s3.put_public_access_block(
            Bucket=BUCKET_NAME,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            })
            print(f"Public access block configuration not found for bucket '{BUCKET_NAME}', remediating now.")
    

   
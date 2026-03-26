# Load my .env file
# Connect to AWS and to S3 console
# Create a S3 Bucket in us-east-2 region

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
s3.create_bucket(ACL='private',
                Bucket=BUCKET_NAME, 
                CreateBucketConfiguration={'LocationConstraint': 'us-east-2'}
                )
print(f"Bucket {BUCKET_NAME} created successfully!")
import boto3
import os  
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

s3 = boto3.client('s3', region_name='us-east-1')

def is_frontend_bucket(bucket_name):
    try: 
        tagging = s3.get_bucket_tagging(Bucket=bucket_name)
        tags = tagging.get('TagSet', [])
        
        for tag in tags:
            if tag['Key'].lower() == 'frontend':
                return True
        return False 
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchTagSet':
            return False
        print(f"Error checking tags for {bucket_name}: {e}")
        return False

def remediate_bucket(bucket_name):
    s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
    )
    print(f"Remediated: '{bucket_name}' is now compliant.")

all_buckets_resp = s3.list_buckets()
print(f"Starting audit of {len(all_buckets_resp['Buckets'])} buckets...\n")

for bucket in all_buckets_resp['Buckets']:
    name = bucket['Name']
    if is_frontend_bucket(name):
        print(f"Skipping: '{name}' is a frontend bucket.")
        continue 
    try:
        check = s3.get_public_access_block(Bucket=name)
        config = check['PublicAccessBlockConfiguration']
        if config.get('BlockPublicPolicy') and config.get('BlockPublicAcls'):
            print(f"Compliant: '{name}' already has public access blocked.")
        else:
            remediate_bucket(name)

    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            print(f"Missing Configuration: '{name}' has no block settings.")
            remediate_bucket(name)
        else:
            print(f"Error auditing {name}: {e}")

print("\nAudit Complete.")
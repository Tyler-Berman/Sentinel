# Connect Cloud Trail Logs with S3 bucket for Sentinel Audit

import boto3
import os
from dotenv import load_dotenv
load_dotenv()

cloudtrail = boto3.client('cloudtrail')
s3_bucket_name = "ai-sentinel-security-reports-2026"

def create_sentinel_trail():
    print(f"Creating CloudTrail: Sentinel-Activity-Log")
    try:
        cloudtrail.create_trail(
            Name='Sentinel-Activity-Log',
            S3BucketName=s3_bucket_name,
            IncludeGlobalServiceEvents=True,
            IsMultiRegionTrail=True
        )

        cloudtrail.start_logging(
            Name='Sentinel-Activity-Log'
        )
        print(f"Cloudtrail is now logging to S3")
    except Exception as e:
        print(f"Error {e}")
create_sentinel_trail()
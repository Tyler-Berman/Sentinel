# Incorporate SNS notifications into the S3 bucket public access settings remediation script, so that when a bucket is found to be non-compliant and remediated, a notification is sent to an SNS topic with details of the remediation action taken.


import boto3
import os  
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')  

sns = boto3.client('sns',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-2'
)
s3 = boto3.client('s3', 
    aws_access_key_id=aws_access_key_id,        
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-2'
)
MY_TOPIC_ARN = os.getenv('TOPIC_ARN')
any_remediations = False
buckets_checked = 0
ALL_BUCKETS = s3.list_buckets()
for bucket in ALL_BUCKETS['Buckets']:
    buckets_checked += 1
    BUCKET_NAME = bucket['Name']
    try:
        SECURITY_CHECK = s3.get_public_access_block(Bucket=BUCKET_NAME)
        PUBLIC_ACCESS = SECURITY_CHECK['PublicAccessBlockConfiguration']    
        PUBLIC_POLICY = PUBLIC_ACCESS['BlockPublicPolicy']
        PUBLIC_ACLS = PUBLIC_ACCESS['BlockPublicAcls']
        if PUBLIC_POLICY == True and PUBLIC_ACLS == True:
            print(f"Public access settings for bucket '{BUCKET_NAME}' are compliant.")
        else: 
            any_remediations = True
            s3.put_public_access_block(
            Bucket=BUCKET_NAME,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            })
            sns.publish(
                TopicArn=MY_TOPIC_ARN,
                Message=f"Public access settings for bucket '{BUCKET_NAME}' have been found to be non-compliant and have been remediated.",
                Subject=f"S3 Security Remediation Notification: Bucket '{BUCKET_NAME}'"
        )
            print(f"Public access settings for bucket '{BUCKET_NAME}' have been remediated to be compliant.")
    
    except s3.exceptions.NoSuchPublicAccessBlockConfiguration:
            any_remediations = True
            s3.put_public_access_block(
            Bucket=BUCKET_NAME,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            })
            sns.publish(
                TopicArn=MY_TOPIC_ARN,
                Message=f"Public access settings for bucket '{BUCKET_NAME}' have been found to be non-compliant and have been remediated.",
                Subject=f"S3 Security Remediation Notification: Bucket '{BUCKET_NAME}'"
            )
            print(f"Public access block configuration not found for bucket '{BUCKET_NAME}', remediating now.")
if not any_remediations:
    sns.publish(
        TopicArn=MY_TOPIC_ARN,
        Message=f"All S3 buckets have been found to be compliant with public access settings. No remediation actions were necessary.",
        Subject=f"S3 Security Remediation Notification: All Buckets Compliant"
    )
print(f"Security audit completed for {buckets_checked} buckets.")
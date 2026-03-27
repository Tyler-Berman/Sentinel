# Create an SNS topic and subscribe to it
# Add my email address to the subscription list
# Use this SNS topic to send notifications to my email address when my S3 security auditor remediates a bucket's public access settings to be compliant.

import boto3
import os  
from dotenv import load_dotenv
load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

SNS = boto3.client('sns',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-2'
)
TOPIC_NAME = 'S3SecurityRemediationNotifications'
TOPIC_CREATION = SNS.create_topic(Name=TOPIC_NAME)
TOPIC_ARN = TOPIC_CREATION['TopicArn']
print(f"{TOPIC_NAME} READY: {TOPIC_ARN}")

EMAIL = os.getenv('NOTIFICATION_EMAIL', 'example@example.com')
SNS.subscribe(
    TopicArn=TOPIC_ARN,
    Protocol='email',
    Endpoint=EMAIL
)
print(f"Subscription request sent to {EMAIL}. Please check your email and confirm the subscription to receive notifications.")
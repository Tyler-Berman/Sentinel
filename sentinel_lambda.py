import json
import boto3
import os
from dotenv import load_dotenv
load_dotenv()

sns = boto3.client('sns')
TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN') 

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            file_key = record['s3']['object']['key']
            
            print(f"Sentinel detected new log: {file_key} in {bucket_name}")

            message = f"Sentinel Security Update: New log file detected.\nBucket: {bucket_name}\nFile: {file_key}"
            
            sns.publish(
                TopicArn=TOPIC_ARN,
                Message=message,
                Subject="Sentinel Security Alert"
            )
            
        return {
            'statusCode': 200,
            'body': json.dumps('Sentinel processed the event successfully!')
        }
    except Exception as e:
        print(f"Error: {e}")
        raise e
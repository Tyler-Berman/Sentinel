import boto3
import os
from dotenv import load_dotenv
load_dotenv()

logs = boto3.client('logs', region_name='us-east-2')

LOG_GROUP_NAME = '/aws/vpc/sentinel-flow-logs'

try:
    print(f"Sentinel Phase 8: Initializing Log Group...")
    logs.create_log_group(logGroupName=LOG_GROUP_NAME)
    
    logs.put_retention_policy(
        logGroupName=LOG_GROUP_NAME,
        retentionInDays=7  
    )
    print(f"SUCCESS: Log Group '{LOG_GROUP_NAME}' created with 7-day retention.")

except logs.exceptions.ResourceAlreadyExistsException:
    print(f"Log Group '{LOG_GROUP_NAME}' already exists. Moving to next step.")
except Exception as e:
    print(f"ERROR: {e}")
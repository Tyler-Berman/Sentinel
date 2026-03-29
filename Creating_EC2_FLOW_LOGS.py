import boto3
import os
from dotenv import load_dotenv
load_dotenv()

ec2 = boto3.client('ec2',
                   region_name='us-east-2')
# Define Variables
VPC_ID = os.getenv('MY_VPC_ID')
LOG_GROUP_NAME = os.getenv('MY_LOG_GROUP_NAME')
ROLE_ARN = os.getenv('MY_ROLE_ARN')

try: 
    # Create flow logs for EC2
    response = ec2.create_flow_logs(
        ResourceIds=[VPC_ID],
        ResourceType='VPC',
        TrafficType='ALL',
        LogDestinationType='cloud-watch-logs',
        LogGroupName=LOG_GROUP_NAME,
        DeliverLogsPermissionArn=ROLE_ARN
    )
    # Success Message
    print(f"SUCCESS: Flow logs enabled ID: {response['FlowLogIds'][0]}")
except Exception as e:
    # Fail Message
    print(f'ERROR: {e}')


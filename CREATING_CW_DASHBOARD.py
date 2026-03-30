import boto3
import os
from dotenv import load_dotenv
load_dotenv()
import json

cw = boto3.client('cloudwatch', region_name='us-east-2')
dashboard_body = {
    "widgets": [
        {
            "type": "log",
            "x": 0,
            "y": 0,
            "width": 24,
            "height": 6,
            "properties": {
                "query": "SOURCE logGroups '/aws/vpc/sentinel-flow-logs'| filterIndex action in [\"REJECT\"] | filterIndex `@data_source_name` in [\"amazon_vpc\"] | fields @timestamp, srcAddr, dstAddr, dstPort, action\n| filter action = \"REJECT\"\n| sort @timestamp desc\n| limit 20\n",
                "queryLanguage": "CWLI",
                "queryBy": "allLogGroups",
                "logGroupPrefixes": {
                    "accountIds": [
                        "All"
                    ],
                    "logGroupPrefix": [],
                    "logClass": "STANDARD"
                },
                "region": "us-east-2",
                "title": "Log group",
                "view": "table"
            }
        },
        {
            "type": "log",
            "x": 0,
            "y": 6,
            "width": 24,
            "height": 6,
            "properties": {
                "query": "SOURCE '/aws/vpc/sentinel-flow-logs' | fields @timestamp, dstPort, action\n| filter action = \"REJECT\"\n| stats count(*) as attackCount by dstPort\n| sort attackCount desc\n| limit 5",
                "queryLanguage": "CWLI",
                "queryBy": "logGroupName",
                "logGroupPrefixes": {
                    "logClass": "STANDARD",
                    "logGroupPrefix": [],
                    "accountIds": []
                },
                "region": "us-east-2",
                "title": "Log group: /aws/vpc/sentinel-flow-logs",
                "view": "pie"
            }
        }
    ]
}
    


try:
    print("Sentinel Phase 9: Deploying Command Center Dashboard...")
    cw.put_dashboard(
        DashboardName='Sentinel-Command-Center',
        DashboardBody=json.dumps(dashboard_body)
    )
    print("SUCCESS: Dashboard 'Sentinel-Command-Center' is live!")
except Exception as e:
    print(f"ERROR: {e}")
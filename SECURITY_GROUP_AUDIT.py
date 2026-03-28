# Check EC2 security groups for open ports
# Edit security group rules to remediate any vulnerabilities found

import boto3
import os
from dotenv import load_dotenv
load_dotenv()

def security_audit_ec2():
    # SCANS EC2 SECURITY GROUPS FOR WORLD-OPEN SSH RULES AND REVOKES THEM IF FOUND
    ec2 = boto3.client('ec2', region_name='us-east-2')
    security_groups = ec2.describe_security_groups()
    for sg in security_groups['SecurityGroups']:
        print(f"Checking: {sg['GroupName']} ({sg['GroupId']})")
        vulnerabilities_found = 0
        
        for direction in ['IpPermissions', 'IpPermissionsEgress']:
            for rule in sg.get(direction, []):
                protocol = rule.get('IpProtocol')
                from_port = rule.get('FromPort')
                to_port = rule.get('ToPort')
                
                is_all_traffic = protocol == '-1'
                has_ssh_port = from_port is not None and from_port <= 22 <= to_port
                
                if is_all_traffic or has_ssh_port:
                    for ip_range in rule.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            vulnerabilities_found += 1
                            print(f"VULNERABILITY CONFIRMED ({direction})! Revoking...")
                            
                            try:
                                params = {
                                    'GroupId': sg['GroupId'],
                                    'IpPermissions': [{
                                        'IpProtocol': protocol,
                                        'IpRanges': [{'CidrIp': ip_range.get('CidrIp')}]
                                    }]
                                }
                                if from_port is not None:
                                    params['IpPermissions'][0]['FromPort'] = from_port
                                    params['IpPermissions'][0]['ToPort'] = to_port

                                if direction == 'IpPermissions':
                                    ec2.revoke_security_group_ingress(**params)
                                else:
                                    ec2.revoke_security_group_egress(**params)
                                print(f"SUCCESS: Rule removed from {sg['GroupName']}.")
                            except Exception as e:
                                print(f"ERROR: {e}")
        if vulnerabilities_found == 0:
            print(f"No vulnerabilities found in {sg['GroupName']}.")
security_audit_ec2()
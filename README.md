# Project Sentinel: AWS Infrastructure Automation
Author: Tyler Berman
Status: In Development (Phase 9: Monitoring Dashboard)

Project Overview: Project Sentinel is a suite of Python-based automation tools designed to manage, monitor and secure AWS cloud resources. This project demonstrates the transition from infrastructure theory (AWS SAA/AIF) to hands-on Infrastructure as Code (IAC) and DevOps practices.

Key Features: 
1. Storage Guardrails (S3)
Automated Hardening: Python scripts to enforce S3 Block Public Access.
Object Auditing: Boto3-powered inventory tools to track and report on bucket contents.

2. Self-Healing Compute (EC2 & Lambda)
Automated Remediation: A serverless "Sentinel" Lambda that scans Security Groups for high-risk rules (Port 22/0.0.0.0/0) and revokes them in real-time.
Alert Aggregation: Intelligent SNS notification logic that batches multiple security findings into a single, actionable report to prevent alert fatigue.

3. Network Surveillance (VPC & CloudWatch)
Traffic Logging: Infrastructure scripts to deploy VPC Flow Logs with custom IAM delivery roles.
Threat Hunting: Integrated CloudWatch Logs Insights queries to identify and visualize unauthorized connection attempts (REJECT logs).

Tech Stack:
Language: Python 3.x
AWS SDK: Boto3
Tools: AWS CLI, Git, Bash
Cloud Services: S3, Lambda, IAM, SNS, Cloudwatch, VPC, EC2
Networking: VPC Flow Logs, Cloudwatch insights

Progress Roadmap:
[X] AWS Account Hardening (MFA, IAM, Budgets)
[X] Local Environment Setup (Python, Boto3)
[X] First S3 Automation Script
[X] Lambda Integration
[X] EC2 security remediation
[X] SNS notifications for security findings
[X] VPC Flow Logs
[X] Cloudwatch dashboard for monitoring
[] AI integration for automated security reports

License:
Distributed under the MIT License. See LICENSE for more information.

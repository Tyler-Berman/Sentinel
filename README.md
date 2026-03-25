# Project Sentinel: AWS Infrastructure Automation
Author: Tyler Berman
Status: In Development (Phase 1: Foundation)

Project Overview: Project Sentinel is a suite of Python-based automation tools designed to manage and secure AWS cloud resources. This project demonstrates the transition from infrastructure theory (AWS SAA/AIF) to hands-on Infrastructure as Code (IAC) and DevOps practices.

Key Features (Phase 1): 
S3 Guard: A Python script using Boto3 to audit S3 buckets for public access and lists active objects.
Lambda Trigger: Basic serverless function setup to automate routine cloud tasks.
Secure Foundation: Implements IAM Best Practices (Least Privilege) and environment variable protection.

Tech Stack:
Language: Python 3.x
AWS SDK: Boto3
Tools: AWS CLI, Git, Bash
Cloud Services: S3, Lambda, IAM

Progress Roadmap:
[X] AWS Account Hardening (MFA, IAM, Budgets)
[X] Local Environment Setup (Python, Boto3)
[] First S3 Automation Script
[] Lambda Integration

License:
Distributed under the MIT License. See LICENSE for more information.

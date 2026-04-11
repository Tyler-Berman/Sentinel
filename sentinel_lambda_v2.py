import boto3
import json
import os
import re 

s3 = boto3.client('s3')
bedrock = boto3.client('bedrock-runtime')
sns = boto3.client('sns')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    file_content = s3.get_object(Bucket=bucket, Key=key)['Body'].read().decode('utf-8')
    
    prompt = (
        "You are a security analyst. Analyze these logs for threats. "
        "Return ONLY a raw JSON object with keys 'threat_level' and 'summary'. "
        "Do not include any conversational text, markdown code blocks, or explanations. "
        f"Logs: {file_content}"
    )
    
    try:
        response = bedrock.invoke_model(
            modelId="amazon.nova-micro-v1:0",
            body=json.dumps({
                "inferenceConfig": {"max_new_tokens": 1000, "temperature": 0.1}, # Added low temperature for stability
                "messages": [{"role": "user", "content": [{"text": prompt}]}]
            })
        )
        result = json.loads(response['body'].read())
        analysis_raw = result['output']['message']['content'][0]['text']
        
        match = re.search(r'\{.*\}', analysis_raw, re.DOTALL)
        if match:
            analysis = match.group(0)
        else:
            analysis = analysis_raw 

    except Exception as e:
        print(f"Bedrock Error: {e}")
        analysis = '{"threat_level": "Low", "summary": "Error calling Bedrock"}'

    s3.put_object(
        Bucket=os.environ['RESULTS_BUCKET'],
        Key=f"analysis-{key}.json",
        Body=analysis
    )
    
    print(f"DEBUG - Cleaned Analysis: {analysis}")
    
    try:
        threat_data = json.loads(analysis)
        if threat_data.get('threat_level', '').lower() == 'high':
            sns.publish(
                TopicArn=os.environ['TOPIC_ARN_2'],
                Message=f"SECURITY ALERT: {threat_data.get('summary', 'No summary provided')}",
                Subject="Sentinel High-Priority Threat Detected"
            )
    except Exception as parse_error:
        print(f"JSON Parse Error: {parse_error} - Raw: {analysis}")

    return {"statusCode": 200, "body": "Analysis Complete"}
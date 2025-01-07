import boto3
import re

def scan_s3_bucket(bucket_name):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name)

    print(f"Scanning bucket: {bucket_name}")
    for obj in response.get('Contents', []):
        key = obj['Key']
        file_obj = s3.get_object(Bucket=bucket_name, Key=key)
        content = file_obj['Body'].read().decode('utf-8')

        # Look for sensitive information
        if re.search(r'\b\d{4}-\d{4}-\d{4}-\d{4}\b', content):  # Example: Credit card pattern
            print(f"Sensitive data found in file: {key}")

        # Check if the file is encrypted
        if 'ServerSideEncryption' not in file_obj:
            print(f"Unencrypted file detected: {key}")

# Run the scanner
scan_s3_bucket('your-bucket-name')
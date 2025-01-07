import boto3
import re
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

class S3Scanner:
    @staticmethod
    def scan_bucket(bucket_name):
        try:
            # Initialize the S3 client with the correct region
            s3 = boto3.client('s3', region_name='us-east-2')

            # Check if the bucket exists and is accessible
            try:
                s3.head_bucket(Bucket=bucket_name)
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    return [f"Bucket '{bucket_name}' does not exist."]
                elif e.response['Error']['Code'] == '403':
                    return [f"Access denied to bucket '{bucket_name}'. Please check your permissions."]
                else:
                    return [f"An error occurred while accessing bucket '{bucket_name}': {e.response['Error']['Message']}"]

            # List objects in the bucket
            response = s3.list_objects_v2(Bucket=bucket_name)
            if 'Contents' not in response:
                return [f"No files found in bucket: {bucket_name}"]

            issues = []
            for obj in response['Contents']:
                key = obj['Key']
                try:
                    file_obj = s3.get_object(Bucket=bucket_name, Key=key)
                    content = file_obj['Body'].read().decode('utf-8', errors='ignore')

                    # Look for sensitive information
                    if re.search(r'\b\d{4}-\d{4}-\d{4}-\d{4}\b', content):  # Example: Credit card pattern
                        issues.append(f"Sensitive data found in file: {key}")

                    # Check if the file is encrypted
                    if 'ServerSideEncryption' not in file_obj:
                        issues.append(f"Unencrypted file detected: {key}")

                except Exception as e:
                    issues.append(f"Error scanning file '{key}': {str(e)}")

            return issues

        except NoCredentialsError:
            return ["AWS credentials not found. Please configure your credentials."]
        except PartialCredentialsError:
            return ["Incomplete AWS credentials. Please check your configuration."]
        except Exception as e:
            return [f"An unexpected error occurred: {str(e)}"]

import boto3
import json
import base64
import requests
import os
from dotenv import load_dotenv

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # Parse the request body into a JSON object
    body = event

    # Get the file content and filename from the request body
    filename = body['filename']
    file_content = base64.b64decode(body['file'])

    # Specify the bucket and file name
    bucket = 'bot-context-txt'  # replace with your bucket name

    # Upload the file to the S3 bucket
    s3.put_object(Body=file_content, Bucket=bucket, Key=filename)

    load_dotenv()

    # Access environment variables
    url = os.environ['URL']


    if check_file_in_bucket(bucket, filename) == 200:
        # Make a GET request to the endpoint
        response = requests.get(url)
        if response.status_code == 200:
            return {
                "statusCode": 200,
                "body": "TXT subido a S3 y GET request a /update-context realizado.",
            }
        else:
            return {
                "statusCode": 500,
                "body": "Error realizando GET request a /update-context.",
            }
    else:
        return {
            "statusCode": 404,
            "body": "TXT no subido a S3.",
        }


def check_file_in_bucket(bucket_name, file_name):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    for obj in bucket.objects.all():
        if obj.key == file_name:
            return 200

    return 404

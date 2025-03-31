import boto3
from django.conf import settings

def get_s3_client():
    """Returns an S3 client"""
    return boto3.client(
        's3',
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY
    )

def upload_to_s3(file, bucket_name, object_name):
    """Uploads a file to S3"""
    s3_client = get_s3_client()
    s3_client.upload_fileobj(file, bucket_name, object_name)
    return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"

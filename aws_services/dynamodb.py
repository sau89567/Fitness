import boto3
from django.conf import settings

def get_dynamodb_table(table_name):
    """Returns a reference to a DynamoDB table"""
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    return dynamodb.Table(table_name)

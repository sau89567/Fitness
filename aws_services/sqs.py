import boto3
from django.conf import settings

def get_sqs_queue(queue_name):
    """Returns an SQS queue"""
    sqs = boto3.resource(
        'sqs',
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    return sqs.get_queue_by_name(QueueName=queue_name)

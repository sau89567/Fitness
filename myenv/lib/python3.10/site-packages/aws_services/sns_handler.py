import boto3
from botocore.exceptions import ClientError, CredentialRetrievalError
from datetime import datetime, timedelta
import time
from django.conf import settings

class SNSHandler:
    def __init__(self, region_name="us-east-1"):
        self.region_name = region_name
        self.topic_name = "FitnessAppUserNotifications"  # Make sure the topic name is correct
        self.topic_arn = None
        self._credentials_expiry = None
        print(f"Initializing SNSHandler for region: {self.region_name}")
        self._initialize_sns_client()

    def _initialize_sns_client(self, retry_count=0):
        """Initialize SNS client with credential refresh handling"""
        try:
            print(f"Initializing SNS client... Attempt {retry_count + 1}")
            session = boto3.Session()
            self.sns_client = session.client('sns', region_name=self.region_name)
            
            # Check if credentials are available
            credentials = session.get_credentials()
            if hasattr(credentials, 'expiry_time'):
                self._credentials_expiry = credentials.expiry_time
            print(f"SNS client initialized successfully.")
        except (ClientError, CredentialRetrievalError) as e:
            if retry_count < 3:
                print(f"Error initializing SNS client (attempt {retry_count + 1}): {e}")
                time.sleep(2 ** retry_count)
                return self._initialize_sns_client(retry_count + 1)
            raise

    def _check_credentials(self):
        """Check if credentials are about to expire and refresh if needed"""
        if self._credentials_expiry and datetime.now() > self._credentials_expiry - timedelta(minutes=5):
            print("Credentials are about to expire, refreshing...")
            self._initialize_sns_client()

    def create_topic(self):
        """Create an SNS topic if it doesn't exist"""
        print(f"Creating SNS topic: {self.topic_name}")
        self._check_credentials()
        try:
            response = self.sns_client.create_topic(Name=self.topic_name)
            self.topic_arn = response['TopicArn']
            print(f"Created SNS topic: {self.topic_arn}")
            return self.topic_arn
        except ClientError as e:
            print(f"Error creating SNS topic: {e}")
            raise

    def get_or_create_topic(self):
        """Get existing topic ARN or create new one"""
        print(f"Fetching or creating SNS topic: {self.topic_name}")
        self._check_credentials()
        try:
            response = self.sns_client.list_topics()
            for topic in response.get('Topics', []):
                if self.topic_name in topic['TopicArn']:
                    self.topic_arn = topic['TopicArn']
                    print(f"Found existing SNS topic: {self.topic_arn}")
                    return self.topic_arn
            print(f"Topic not found. Creating new topic...")
            return self.create_topic()
        except ClientError as e:
            print(f"Error listing SNS topics: {e}")
            raise

    def publish_confirmation(self, email_address, message):
        """Publish a confirmation message to the topic"""
        print(f"Publishing message to SNS topic for email {email_address}.")
        self._check_credentials()
        try:
            if not self.topic_arn:
                self.get_or_create_topic()

            response = self.sns_client.publish(
                TopicArn=self.topic_arn,
                Message=message,
                Subject="Fitness App Notification",
                MessageAttributes={
                    'email': {
                        'DataType': 'String',
                        'StringValue': email_address
                    }
                }
            )
            print(f"Message published to SNS topic for {email_address}. MessageId: {response['MessageId']}")
            return response['MessageId']
        except ClientError as e:
            print(f"Error publishing confirmation: {e}")
            raise

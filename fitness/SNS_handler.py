# import boto3
# from botocore.exceptions import ClientError, CredentialRetrievalError
# from datetime import datetime, timedelta
# import time

# class SNSHandler:
#     def __init__(self, region_name="us-east-1"):
#         self.region_name = region_name
#         self.topic_name = "FitnessPlanSubscriptions"  # Topic name for fitness plans
#         self.topic_arn = None
#         self._credentials_expiry = None
#         self._initialize_sns_client()

#     def _initialize_sns_client(self, retry_count=0):
#         """Initialize SNS client with credential refresh handling"""
#         try:
#             session = boto3.Session()
#             self.sns_client = session.client('sns', region_name=self.region_name)

#             # Get credentials expiry time (if using temporary credentials)
#             credentials = session.get_credentials()
#             if hasattr(credentials, 'expiry_time'):
#                 self._credentials_expiry = credentials.expiry_time

#         except (ClientError, CredentialRetrievalError) as e:
#             if retry_count < 3:  # Retry up to 3 times
#                 print(f"Error initializing SNS client (attempt {retry_count + 1}): {e}")
#                 time.sleep(2 ** retry_count)  # Exponential backoff
#                 return self._initialize_sns_client(retry_count + 1)
#             raise

#     def _check_credentials(self):
#         """Check if credentials are about to expire and refresh if needed"""
#         if self._credentials_expiry and datetime.now() > self._credentials_expiry - timedelta(minutes=5):
#             print("Credentials about to expire, refreshing...")
#             self._initialize_sns_client()

#     def get_or_create_topic(self):
#         """Get existing topic ARN or create a new one"""
#         self._check_credentials()
#         try:
#             # List existing topics
#             response = self.sns_client.list_topics()
#             for topic in response.get('Topics', []):
#                 if self.topic_name in topic['TopicArn']:
#                     self.topic_arn = topic['TopicArn']
#                     return self.topic_arn
            
#             # If topic does not exist, create a new one
#             response = self.sns_client.create_topic(Name=self.topic_name)
#             self.topic_arn = response['TopicArn']
#             print(f"Created new SNS topic: {self.topic_arn}")
#             return self.topic_arn
#         except ClientError as e:
#             print(f"Error getting/creating SNS topic: {e}")
#             raise

#     def publish_confirmation(self, email_address, order_details):
#         """Publish a confirmation message to the topic"""
#         self._check_credentials()
#         try:
#             if not self.topic_arn:
#                 self.get_or_create_topic()  # Ensure topic is available

#             message = f"""
#             Thank you for subscribing to our fitness plan!

#             Plan Details:
#             - Plan Type: {order_details.get('plan_type', 'N/A')}
#             - Customer Name: {order_details.get('customer_name', 'N/A')}
#             - Expected Delivery: {order_details.get('delivery_time', 'Within 1 hour')}
#             """

#             response = self.sns_client.publish(
#                 TopicArn=self.topic_arn,
#                 Message=message,
#                 Subject=f"Fitness Plan Subscription Confirmation - {order_details.get('order_id', '')}",
#                 MessageAttributes={
#                     'email': {
#                         'DataType': 'String',
#                         'StringValue': email_address
#                     }
#                 }
#             )
#             print(f"Published confirmation to {email_address}")
#             return response['MessageId']
#         except ClientError as e:
#             if e.response['Error']['Code'] == 'ExpiredTokenException':
#                 self._initialize_sns_client()
#                 return self.publish_confirmation(email_address, order_details)
#             print(f"Error publishing confirmation: {e}")
#             raise

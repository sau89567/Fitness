import boto3
from aws_services.sns_handler import SNSHandler  # Import your SNSHandler class

def test_sns_handler():
    try:
        print("Initializing SNSHandler...")
        sns_handler = SNSHandler(region_name="us-east-1")  # Initialize SNSHandler with the region you are using

        print("Getting or creating the SNS topic...")
        topic_arn = sns_handler.get_or_create_topic()  # Get existing topic or create a new one
        print(f"SNS Topic ARN: {topic_arn}")

        # Now, let's send a test notification
        test_email = "your-email@example.com"  # Replace with an email address you want to send the test to
        test_message = "This is a test message from SNSHandler!"
        print("Publishing test message to SNS topic...")
        message_id = sns_handler.publish_confirmation(test_email, test_message)
        print(f"Test message sent successfully. Message ID: {message_id}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_sns_handler()

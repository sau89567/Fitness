import boto3
from django.http import HttpResponse

AWS_REGION = "us-east-1"
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

def check_django_sessions_table_exists():
    """Checks if the django-sessions table exists in DynamoDB."""
    try:
        table = dynamodb.Table("django-sessions")
        table.load()  # Attempt to load the table
        print("✅ django-sessions table exists!")
        return True
    except Exception as e:
        print("❌ django-sessions table does not exist.")
        return False

def create_django_sessions_table():
    """Creates the django-sessions table in DynamoDB."""
    try:
        table = dynamodb.create_table(
            TableName="django-sessions",
            KeySchema=[{"AttributeName": "SessionId", "KeyType": "HASH"}],  # Primary key
            AttributeDefinitions=[{"AttributeName": "SessionId", "AttributeType": "S"}],  # String type
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},  # Throughput settings
        )
        print("⏳ Waiting for django-sessions table to be created...")
        table.wait_until_exists()
        print("✅ django-sessions table created successfully!")
    except Exception as e:
        print(f"⚠️ Error creating django-sessions table: {e}")

def setup_dynamodb(request):
    """Setup django-sessions table if it doesn't exist."""
    if not check_django_sessions_table_exists():
        create_django_sessions_table()

    return HttpResponse("DynamoDB table 'django-sessions' is set up.")

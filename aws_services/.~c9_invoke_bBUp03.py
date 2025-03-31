import boto3
from botocore.exceptions import ClientError
from django.conf import settings

def get_dynamodb_resource():
    return boto3.resource(
        'dynamodb',
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

def table_exists(table_name):
    """Check if a DynamoDB table exists."""
    dynamodb = get_dynamodb_resource()
    try:
        table = dynamodb.Table(table_name)
        table.load()  # Triggers ClientError if table doesn't exist
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        else:
            raise  # Re-raise unexpected errors

def create_table_if_not_exists(table_name, key_schema, attribute_definitions, provisioned_throughput):
    """Create a DynamoDB table if it doesn't exist."""
    dynamodb = get_dynamodb_resource()
    
    if table_exists(table_name):
        print(f"✅ Table '{table_name}' already exists.")
        return dynamodb.Table(table_name)

    # Create the table
    print(f"🚧 Creating table '{table_name}'...")
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput=provisioned_throughput
    )

    # Wait until it's active
    table.wait_until_exists()
    print(f"✅ Table '{table_name}' created and ready to use.")
    return table
    
def get_dynamodb_table(table_name):
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(table_name)

def store_user_in_dynamodb(username, email):
    table = get_dynamodb_table("Users")  # Your actual table name
    table.put_item(Item={
        'username': username,
        'email': email
    })

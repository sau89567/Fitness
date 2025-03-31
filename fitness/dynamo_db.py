# import boto3
# from django.conf import settings

# # Initialize DynamoDB resource
# dynamodb = boto3.resource(
#     "dynamodb",
#     region_name='us-east-1',
#     aws_access_key_id='ASIARZNDPJ4NL6TCWAOL',
#     aws_secret_access_key='96rXOWFFrZJqmY22WlD4Dce5QUdmuL6db3TONWmV',
# )

# def get_table(table_name):
#     """Returns a reference to the specified DynamoDB table."""
#     return dynamodb.Table(table_name)
    
    
    
# def create_table():
#     """Creates a DynamoDB table if it does not exist."""
#     table_name = "django-sessions"
    
#     existing_tables = [table.name for table in dynamodb.tables.all()]
#     if table_name in existing_tables:
#         print(f"✅ Table '{table_name}' already exists.")
#         return
    
#     table = dynamodb.create_table(
#         TableName=table_name,
#         KeySchema=[{"AttributeName": "SessionId", "KeyType": "HASH"}],
#         AttributeDefinitions=[{"AttributeName": "SessionId", "AttributeType": "S"}],
#         ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
#     )
    
#     print(f"⏳ Creating table '{table_name}', please wait...")
#     table.wait_until_exists()
#     print(f"✅ Table '{table_name}' created successfully!")


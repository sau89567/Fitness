import boto3
from botocore.exceptions import ClientError
import uuid
import bcrypt
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date
from boto3.dynamodb.conditions import Key, Attr

session = boto3.Session()
dynamodb = session.resource("dynamodb")

table_name = "Users"

def create_users_table():
    try:
        existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
        if table_name not in existing_tables:
            print(f"🔧 Creating DynamoDB table: {table_name}...")
            table = dynamodb.create_table(
                TableName=table_name,
                AttributeDefinitions=[
                    {"AttributeName": "id", "AttributeType": "S"},
                    {"AttributeName": "account_id", "AttributeType": "S"},
                ],
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                BillingMode="PAY_PER_REQUEST",
                GlobalSecondaryIndexes=[
                    {
                        "IndexName": "AccountIdIndex",
                        "KeySchema": [{"AttributeName": "account_id", "KeyType": "HASH"}],
                        "Projection": {"ProjectionType": "ALL"},
                    }
                ],
            )
            table.wait_until_exists()
            print(f"✅ Table '{table_name}' created.")
        else:
            ensure_gsi_exists()
    except ClientError as e:
        print(f"⚠️ Error creating table: {e}")

def ensure_gsi_exists():
    table = dynamodb.Table(table_name)
    indexes = table.global_secondary_indexes or []
    existing_index_names = [idx["IndexName"] for idx in indexes]

    if "AccountIdIndex" not in existing_index_names:
        print("⚠️ Creating missing GSI...")
        try:
            dynamodb.meta.client.update_table(
                TableName=table_name,
                AttributeDefinitions=[{"AttributeName": "account_id", "AttributeType": "S"}],
                GlobalSecondaryIndexUpdates=[
                    {
                        "Create": {
                            "IndexName": "AccountIdIndex",
                            "KeySchema": [{"AttributeName": "account_id", "KeyType": "HASH"}],
                            "Projection": {"ProjectionType": "ALL"},
                        }
                    }
                ],
            )
            print("✅ AccountIdIndex creation requested.")
        except ClientError as e:
            print(f"⚠️ Error creating GSI: {e}")

create_users_table()

class UserModel:
    table = dynamodb.Table(table_name)
   

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(input_password, hashed_password):
        return bcrypt.checkpw(input_password.encode("utf-8"), hashed_password.encode("utf-8"))

    @classmethod
    def create_user(cls, username, email, password, role="user"):
        user_id = cls.generate_uuid()
        account_id = cls.generate_uuid()
        hashed_pw = cls.hash_password(password)

        try:
            cls.table.put_item(
                Item={
                    "id": user_id,
                    "username": username,
                    "email": email,
                    "password": hashed_pw,
                    "role": role,
                    "account_id": account_id,
                }
            )
            return user_id, account_id
        except ClientError as e:
            print(f"⚠️ Error saving user: {e}")
            return None, None

    @classmethod
    def get_user_by_email(cls, email):
        try:
            response = cls.table.scan(
                FilterExpression=Attr("email").eq(email)
            )
            items = response.get("Items", [])
            return items[0] if items else None
        except ClientError as e:
            print(f"⚠️ Error fetching user by email: {e}")
            return None

    @classmethod
    def get_user_by_account_id(cls, account_id):
        try:
            response = cls.table.query(
                IndexName="AccountIdIndex",
                KeyConditionExpression=Key("account_id").eq(account_id)
            )
            items = response.get("Items", [])
            return items[0] if items else None
        except ClientError as e:
            print(f"⚠️ Error fetching user by account ID: {e}")
            return None

class FitnessClass(models.Model):
    title = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)
    duration = models.IntegerField(help_text="Duration in minutes")
    image = models.ImageField(upload_to='fitness_classes/')
    description = models.TextField()

def __str__(self):
        return self.title

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    
def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.plan:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        self.is_active = date.today() <= self.end_date
        super().save(*args, **kwargs)

def __str__(self):
    
        return f"{self.user.username} - {self.plan.name if self.plan else 'No Plan'}"
        
from django.contrib.auth.decorators import login_required

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

from datetime import date

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Set the end date based on the plan's duration
        if self.plan:
            if not self.end_date:  # If end_date is None, calculate it
                self.end_date = self.start_date + timedelta(days=self.plan.duration_days)

        # Check if the subscription is active
        if self.end_date:
            self.is_active = date.today() <= self.end_date
        else:
            self.is_active = False  # If end_date is None, the subscription is not active

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name if self.plan else 'No Plan'}"

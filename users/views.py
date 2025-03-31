from django.http import HttpResponse
from users.dynamodb_service import create_django_sessions_table, check_django_sessions_table_exists

def setup_dynamodb(request):
    """Setup django-sessions table if it doesn't exist."""
    if not check_django_sessions_table_exists():
        create_django_sessions_table()

    return HttpResponse("DynamoDB table 'django-sessions' is set up.")
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Payments'

    def ready(self):
        # This runs automatically when Django starts
        from aws_services.dynamodb_setup import setup_dynamodb_tables
        setup_dynamodb_tables()
from django.apps import AppConfig

class FitnessConfig(AppConfig):
    name = 'fitness'


from django.urls import path
from . import views

urlpatterns = [
    path('setup_dynamodb/', views.setup_dynamodb, name='setup_dynamodb'),
]

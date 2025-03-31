"""
URL configuration for fitness project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views  
from django.contrib import admin
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
# from .views import fetch_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('workouts.urls')), 
    path("login.html/", views.user_login, name="login"), 
    path("signup/", views.user_signup, name="signup"), 
    path("admin-login/", views.admin_login, name="admin_login"),
    path("home/", views.admin_login, name="admin_dashboard"),
    path("dashboard/", views.user_dashboard, name="user_dashboard"), 
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('subscription/', views.subscription_view, name='subscription'),
    path('profile/', views.profile_view, name='profile'),
    path('choose-plan/', views.choose_plan, name='choose_plan'),
    path('checkout/<int:plan_id>/', views.checkout, name='checkout'),
    path('process_payment/<int:plan_id>/', views.process_payment, name='process_payment'),  
    path('payment_success/<int:plan_id>/', views.payment_success, name='payment_success'),
    path("uploads/", include("uploads.urls")),
    path("upload-file/", views.upload_file, name="upload_file"),
   # path("fetch-data/", fetch_data, name="fetch_data"),
   # path("signup/", signup_view, name="signup"),
   # path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
   # path("user-dashboard/", user_dashboard, name="user_dashboard"),
    path('', views.index, name='index') # Include workouts app
    #path('users/', include('users.urls')),  # Include user authentication
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

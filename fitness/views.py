from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserSubscription, SubscriptionPlan
import stripe
from django.http import JsonResponse
#from .dynamo_db import get_table
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from workouts.models import Workout
def index(request):
    return render(request, 'index.html')

def user_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please use another.")
            return redirect("signup")

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)  # Auto-login after registration
        return redirect("user_dashboard")  # Redirect to user dashboard after signup

    return render(request, "signup.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if user exists in database
        if not User.objects.filter(username=username).exists():
            return redirect('/login/?show_signup_prompt=True')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.is_superuser:
                return redirect("admin_dashboard")  # Admin panel
            else:
                return redirect("user_dashboard")   # Normal user panel
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, "login.html")
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the admin user
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:  # Check if the user is an admin
            login(request, user)
            return redirect("admin_dashboard")  # Redirect to admin panel
        else:
            messages.error(request, "Invalid admin credentials. Please try again.")

    return render(request, "admin_login.html")

@login_required
def user_dashboard(request):
    workouts = Workout.objects.all()
    return render(request, "user_dashboard.html",{'workouts':workouts})

@login_required
def subscription_view(request):
    return render(request, 'subscription.html')


@login_required
def profile_view(request):
    return render(request, 'profile.html')



@login_required
def subscription_view(request):
    try:
        subscription = UserSubscription.objects.get(user=request.user)
    except UserSubscription.DoesNotExist:
        subscription = None

    return render(request, 'subscription.html', {'subscription': subscription})

@login_required
def choose_plan(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'choose_plan.html', {'plans': plans})



stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request, plan_id):
    plan = SubscriptionPlan.objects.get(id=plan_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': plan.name},
                'unit_amount': int(plan.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(f"/payment_success/{plan.id}/"),
        cancel_url=request.build_absolute_uri("/subscription/"),
    )

    return redirect(session.url)

@login_required
def payment_success(request, plan_id):
    plan = SubscriptionPlan.objects.get(id=plan_id)
    
    subscription, created = UserSubscription.objects.get_or_create(user=request.user)
    subscription.plan = plan
    subscription.save()

    return redirect('subscription')

def checkout(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    return render(request, 'checkout.html', {
        'plan': plan,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY  # Add this to settings.py
    })

def process_payment(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    
    # Simulate payment processing (you can integrate Stripe later)
    print(f"Processing payment for {plan.name} - ${plan.price}")
    
    # Redirect user to home page or success page after payment
    return redirect('user_dashboard')  


from django.http import JsonResponse
from aws_services.dynamodb import get_dynamodb_table

def fetch_data(request):
    table = get_dynamodb_table("your-dynamodb-table-name")
    response = table.scan()
    return JsonResponse(response["Items"], safe=False)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@csrf_exempt  # Temporarily disable CSRF for testing
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
        return JsonResponse({"message": "File uploaded successfully!", "file_name": file_name})
    
    return JsonResponse({"error": "No file uploaded"}, status=400)


# def fetch_data(request):
#     """Fetches data from DynamoDB table."""
#     table = get_table("your-table-name")
    
#     try:
#         response = table.scan()  # Fetch all records
#         items = response.get("Items", [])
#         return JsonResponse({"data": items}, safe=False)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)


# import boto3
# from django.conf import settings

# # Connect to DynamoDB
# dynamodb = boto3.resource(
#     'dynamodb',
#     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#     region_name=settings.AWS_REGION_NAME,
# )

# # Create a reference to the DynamoDB Table
# workout_table = dynamodb.Table(settings.AWS_DYNAMODB_TABLE_NAME)

# # Function to add workout data
# def add_workout_to_dynamodb(title, difficulty, description):
#     response = workout_table.put_item(
#         Item={
#             'title': title,
#             'difficulty': difficulty,
#             'description': description,
#         }
#     )
#     return response

# # Function to retrieve all workouts
# def get_workouts_from_dynamodb():
#     response = workout_table.scan()
#     return response.get('Items', [])

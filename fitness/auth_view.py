# fitness/auth_views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            return redirect('/login/?show_signup_prompt=True')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("user_dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")



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
    return render(request, "user_dashboard.html")
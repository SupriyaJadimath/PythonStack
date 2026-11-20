
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# REGISTRATION
def register_page(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check password
        if password != confirm_password:
            return render(request, "accounts/register.html", {
                'error': "Passwords do not match!"
            })

        # Check existing username
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                'error': "Username already exists!"
            })

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'accounts/registration.html')


# LOGIN
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, "accounts/login.html", {
                'error': "Invalid username or password"
            })

    return render(request, 'accounts/login.html')


# DASHBOARD
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


# LOGOUT
def logout_page(request):
    if request.method == "POST":
        logout(request)

    return redirect('login')

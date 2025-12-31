from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "users/index.html")


def signup_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        confirm = request.POST["confirm_password"]

        if password != confirm:
            return render(
                request, "users/signup.html", {"error": "Passwords do not match"}
            )

        if User.objects.filter(username=email).exists():
            return render(
                request, "users/signup.html", {"error": "Email already exists"}
            )

        User.objects.create_user(username=email, email=email, password=password)
        return redirect("login")

    return render(request, "users/signup.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        return render(request, "users/login.html", {"error": "Invalid credentials"})

    return render(request, "users/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("index")



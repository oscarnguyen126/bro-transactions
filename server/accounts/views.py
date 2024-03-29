from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


def home(request):
       return render(request, 'home.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user.is_active:
            return render(request, 'home.html')
        else:
            return render(request, 'accounts/login.html')


def register(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_repeat = request.POST.get('password_repeat')

    if request.method == 'POST':
        if not email or not password or not password_repeat:
            return render(request, 'accounts/register.html')

        user_already_existed = len(User.objects.filter(email=email)) > 0
        if user_already_existed:
            return render(request, 'accounts/error.html')

        if password != password_repeat:
            return render(request, 'accounts/error1.html')

        user = User()
        user.email = email
        user.password = make_password(password)
        user.username = email.split("@")[0]
        user.save()
        return redirect('homepage')
    else:
        return render(request, 'accounts/register.html')


def log_out(request):
    request.session.flush()
    return redirect('homepage')

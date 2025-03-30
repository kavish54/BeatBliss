from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from .models import User
from genreApp.templates import genreApp

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            return redirect('sign-up')
    else:
        form = RegisterForm()
    return render(request, 'loginApp/sign-up.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('genreApp/genre-home')
    else:
        form = LoginForm()
    return render(request, 'sign-in.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('sign-in')

def home_view(request):
    return render(request, 'genreApp/genre-home.html')


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from profileApp.models import Profile
from .forms import RegisterForm, LoginForm

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  
        user.save()
        Profile.objects.create(user=user)
        request.session['current_user'] = form.cleaned_data['email']
        return redirect('genreHome')  
    return render(request, 'loginApp/sign-up.html', {'form': form})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['username']  
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)  

        if user:
            request.session['current_user'] = email
            login(request, user)
            return redirect('genreHome')
        else:
            print("Authentication failed!") 
    return render(request, 'loginApp/sign-in.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, 'genreApp/genre-home.html')

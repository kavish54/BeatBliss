# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate, logout

# from profileApp.models import Profile
# from .forms import RegisterForm, LoginForm

# def register_view(request):
#     form = RegisterForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         user = form.save(commit=False)
#         user.set_password(form.cleaned_data['password'])  
#         user.save()
#         Profile.objects.create(user=user)
#         request.session['current_user'] = form.cleaned_data['email']
#         return redirect('genreHome')  
#     return render(request, 'loginApp/sign-up.html', {'form': form})

# def login_view(request):
#     form = LoginForm(request, data=request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         email = form.cleaned_data['username']  
#         password = form.cleaned_data['password']
#         user = authenticate(request, username=email, password=password)  

#         if user:
#             request.session['current_user'] = email
#             login(request, user)
#             return redirect('genreHome')
#         else:
#             print("Authentication failed!") 
#     return render(request, 'loginApp/sign-in.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     return redirect('login')

# def home_view(request):
#     return render(request, 'genreApp/genre-home.html')

# main
# import requests
# from django.http import JsonResponse
# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate, logout
# from profileApp.models import Profile
# from .forms import RegisterForm, LoginForm

# # Abstract API Key (Replace with your own API Key)
# API_KEY = "f5e8fa9261d5493a8c8880327336d18e"  # Get from Abstract API (https://www.abstractapi.com/email-verification-validation-api)

# # Email verification view
# def verify_real_email(request):
#     email = request.GET.get('email')
#     if not email:
#         return JsonResponse({'status': 'error', 'message': 'Email is required'}, status=400)

#     response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY}&email={email}")
#     data = response.json()

#     if data.get("deliverability") == "DELIVERABLE":
#         return JsonResponse({'status': 'valid', 'message': '✅ Email is valid and exists'})
#     else:
#         return JsonResponse({'status': 'invalid', 'message': '❌ This email does not exist!'})

# # Signup view
# def register_view(request):
#     form = RegisterForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         user = form.save(commit=False)
#         user.set_password(form.cleaned_data['password'])  
#         user.save()
#         Profile.objects.create(user=user)
#         request.session['current_user'] = form.cleaned_data['email']
#         return redirect('login')
  
#     return render(request, 'loginApp/sign-up.html', {'form': form})

# # Login view
# def login_view(request):
#     form = LoginForm(request, data=request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         email = form.cleaned_data['username']  
#         password = form.cleaned_data['password']
#         user = authenticate(request, username=email, password=password)  

#         if user:
#             request.session['current_user'] = email
#             login(request, user)
#             return redirect('genreHome')
#     return render(request, 'loginApp/sign-in.html', {'form': form})

# # Logout view
# def logout_view(request):
#     logout(request)
#     return redirect('login')

# # Home view
# def home_view(request):
#     return render(request, 'genreApp/genre-home.html')


# Main 2
# import requests
# from django.http import JsonResponse
# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate, logout
# from profileApp.models import Profile
# from .forms import RegisterForm, LoginForm

# # Abstract API Key (Replace with your own API Key)
# API_KEY = "f5e8fa9261d5493a8c8880327336d18e"  # Get from Abstract API (https://www.abstractapi.com/email-verification-validation-api)

# # Email verification view
# def verify_real_email(request):
#     email = request.GET.get('email')
#     if not email:
#         return JsonResponse({'status': 'error', 'message': 'Email is required'}, status=400)

#     response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY}&email={email}")
#     data = response.json()

#     if data.get("deliverability") == "DELIVERABLE":
#         return JsonResponse({'status': 'valid', 'message': '✅ Email is valid and exists'})
#     else:
#         return JsonResponse({'status': 'invalid', 'message': '❌ This email does not exist!'})

# # Signup view
# def register_view(request):
#     form = RegisterForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         email = form.cleaned_data['email']  # Get the email from the form data

#         # Verify email using the Abstract API
#         response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY}&email={email}")
#         data = response.json()

#         if data.get("deliverability") == "DELIVERABLE":  # If the email is valid
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])  # Hash the password
#             user.save()  # Save the user to the database
#             Profile.objects.create(user=user)  # Create the user profile
            
#             request.session['current_user'] = email  # Store the email in session
#             return redirect('login')  # Redirect to the login page
#         else:
#             return JsonResponse({'status': 'invalid', 'message': '❌ This email does not exist!'}, status=400)

#     return render(request, 'loginApp/sign-up.html', {'form': form})

# # Login view
# def login_view(request):
#     form = LoginForm(request, data=request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         email = form.cleaned_data['username']  # Get the email (username) from the form
#         password = form.cleaned_data['password']
#         user = authenticate(request, username=email, password=password)  # Authenticate the user

#         if user:
#             request.session['current_user'] = email  # Store the email in session
#             login(request, user)  # Log the user in
#             return redirect('genreHome')  # Redirect to the genre home page
#     return render(request, 'loginApp/sign-in.html', {'form': form})

# # Logout view
# def logout_view(request):
#     logout(request)
#     return redirect('login')  # Redirect to login after logging out

# # Home view
# def home_view(request):
#     return render(request, 'genreApp/genre-home.html')

# Main 3
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from profileApp.models import Profile
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages

# Abstract API Key (Replace with your own API Key)
API_KEY = "f5e8fa9261d5493a8c8880327336d18e"  # Get from Abstract API

# Email verification view
def verify_real_email(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email is required'}, status=400)

    response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY}&email={email}")
    data = response.json()

    if data.get("deliverability") == "DELIVERABLE":
        return JsonResponse({'status': 'valid', 'message': '✅ Email is valid and exists'})
    else:
        return JsonResponse({'status': 'invalid', 'message': '❌ This email does not exist!'})

# Signup view
def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']  # Get the email from the form data

        # Verify email using the Abstract API
        response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY}&email={email}")
        data = response.json()

        if data.get("deliverability") == "DELIVERABLE":  # If the email is valid
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save the user to the database
            Profile.objects.create(user=user)  # Create the user profile

            request.session['current_user'] = email  # Store the email in session
            return redirect('login')  # Redirect to the login page
        else:
            return JsonResponse({'status': 'invalid', 'message': '❌ This email does not exist!'}, status=400)

    return render(request, 'loginApp/sign-up.html', {'form': form})

# Login view
def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['username']  # Get the email (username) from the form
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)  # Authenticate the user

        if user:
            request.session['current_user'] = email  # Store the email in session
            login(request, user)  # Log the user in
            return redirect('genreHome')  # Redirect to the genre home page
    return render(request, 'loginApp/sign-in.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logging out

# Home view
def home_view(request):
    return render(request, 'genreApp/genre-home.html')

# Password Reset View
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = get_user_model().objects.get(email=email)
                # Generate token and UID
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode())

                # Construct password reset URL
                reset_url = request.build_absolute_uri(
                    f"http://127.0.0.1:8000/password-reset/{uid}/{token}/"
                )

                # Send password reset email
                send_mail(
                    'Password Reset Request',
                    f'Click here to reset your password: {reset_url}',
                    'noreply@yourdomain.com',
                    [email],
                    fail_silently=False,
                )

                # ✅ Show success message instead of redirecting
                messages.success(request, "✅ Password reset link has been sent to your email.")
            except get_user_model().DoesNotExist:
                messages.error(request, "❌ No account found with this email.")
    
    else:
        form = PasswordResetForm()

    return render(request, 'loginApp/password_reset.html', {'form': form})

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Your password has been successfully reset!")
                return redirect("login")
        else:
            form = SetPasswordForm(user)
        return render(request, "loginApp/password_reset_confirm.html", {"form": form})
    else:
        messages.error(request, "❌ The password reset link is invalid or has expired.")
        return redirect("password_reset")
    
    
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']  # ID is auto-generated, so no need to include it

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email ID")

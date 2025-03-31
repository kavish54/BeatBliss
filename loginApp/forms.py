from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, error_messages={
        'required': "Password is required.",
        'min_length': "Password must be at least 6 characters long."
    })

    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        error_messages = {
            'name': {'required': "Name is required."},
            'email': {'required': "Email is required.", 'unique': "This email is already in use."},
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email ID",
        error_messages={'required': 'Email is required.', 'invalid': 'Enter a valid email.'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={'required': 'Password is required.'}
    )
    
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive. Please contact support.")

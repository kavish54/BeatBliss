# from django import forms
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class RegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, min_length=6, error_messages={
#         'required': "Password is required.",
#         'min_length': "Password must be at least 6 characters long."
#     })

#     class Meta:
#         model = User
#         fields = ['name', 'email', 'password']
#         error_messages = {
#             'name': {'required': "Name is required."},
#             'email': {'required': "Email is required.", 'unique': "This email is already in use."},
#         }

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("An account with this email already exists.")
#         return email

# class LoginForm(AuthenticationForm):
#     username = forms.EmailField(
#         label="Email ID",
#         error_messages={'required': 'Email is required.', 'invalid': 'Enter a valid email.'}
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput,
#         error_messages={'required': 'Password is required.'}
#     )
    
#     def confirm_login_allowed(self, user):
#         if not user.is_active:
#             raise forms.ValidationError("This account is inactive. Please contact support.")


# Main
# from django import forms
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class RegisterForm(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
#         min_length=6,
#         error_messages={
#             'required': "Password is required.",
#             'min_length': "Password must be at least 6 characters long."
#         }
#     )

#     class Meta:
#         model = User
#         fields = ['name', 'email', 'password']
#         error_messages = {
#             'name': {'required': "Name is required."},
#             'email': {'required': "Email is required.", 'unique': "This email is already in use."},
#         }
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
#             'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
#         }

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("An account with this email already exists.")
#         return email

#     def clean_name(self):
#         name = self.cleaned_data.get('name')
#         if User.objects.filter(name=name).exists():
#             raise forms.ValidationError("This username is already taken. Please choose another.")
#         return name


# class LoginForm(AuthenticationForm):
#     username = forms.EmailField(
#         label="Email ID",
#         widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
#         error_messages={'required': 'Email is required.', 'invalid': 'Enter a valid email.'}
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
#         error_messages={'required': 'Password is required.'}
#     )
    
#     def confirm_login_allowed(self, user):
#         if not user.is_active:
#             raise forms.ValidationError("This account is inactive. Please contact support.")


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        min_length=6,
        error_messages={
            'required': "Password is required.",
            'min_length': "Password must be at least 6 characters long."
        }
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        error_messages = {
            'name': {'required': "Name is required."},
            'email': {'required': "Email is required.", 'unique': "This email is already in use."},
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if User.objects.filter(name=name).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return name


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email ID",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        error_messages={'required': 'Email is required.', 'invalid': 'Enter a valid email.'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        error_messages={'required': 'Password is required.'}
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive. Please contact support.")

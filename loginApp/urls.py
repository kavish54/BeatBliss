# from django.urls import path
# from .views import register_view, login_view, logout_view, home_view
# from django.contrib.auth.views import LogoutView

# urlpatterns = [
#     path('register/', register_view, name='register'),
#     path('login/', login_view, name='login'),
#     path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
#     path('', home_view, name='home'),
# ]

from django.urls import path
from .views import register_view, login_view, logout_view, home_view ,verify_real_email,password_reset_view,password_reset_confirm_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home'),
    path('verify-real-email/', verify_real_email, name='verify-real-email'),  # Email validation before registration
    path('password-reset/', password_reset_view, name='password_reset'),
    path('password-reset/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),


]


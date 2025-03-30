from django.urls import path
from .views import register_view, login_view, logout_view, home_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', home_view, name='home'),
   
]

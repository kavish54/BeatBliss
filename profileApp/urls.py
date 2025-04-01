from django.urls import path
from .views import profilePage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('profile/',profilePage,name="profile-page"),
]

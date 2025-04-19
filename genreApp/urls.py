from django.urls import path
from . import views

urlpatterns = [
    path('genreHome/',views.genreHome,name='genreHome'),
    path("result/", views.genreHome, name="genreResult"),
    path("", views.home, name="home"),
]
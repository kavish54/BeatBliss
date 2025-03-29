from django.urls import path
from . import views

urlpatterns = [
    path('',views.genreHome,name='genreHome'),
    path("result/", views.genreHome, name="genreResult")
]
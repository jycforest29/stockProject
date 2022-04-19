from django.urls import path
from . import views

urlpatterns = [
    path('newsPost/', views.newsPost, name = 'newsPost'),
]
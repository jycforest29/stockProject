from django.urls import path
from . import views

urlpatterns = [
    path('detailNewsPost/', views.detailNewsPost, name = 'detailNewsPost'),
]
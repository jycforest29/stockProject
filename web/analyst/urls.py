from django.urls import path
from . import views

urlpatterns = [
    path('analystPost/', views.analystPost, name = 'analystPost'),
] 
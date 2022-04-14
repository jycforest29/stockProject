from django.urls import path
from . import views

urlpatterns = [
    path('detailanalystPost/', views.detailanalystPost, name = 'detailanalystPost'),
] 
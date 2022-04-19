from django.urls import path
from . import views

urlpatterns = [
    path('detailPost/', views.detailPost, name = 'detailPost'),
]
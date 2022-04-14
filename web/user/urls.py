from django.urls import path
from . import views

urlpatterns = [
    path('signOut/', views.signOut, name = 'signOut'),
    path('signIn/', views.signIn, name = 'signIn'),
    path('signIn/signUp/', views.signUp, name = 'signUp'),
]
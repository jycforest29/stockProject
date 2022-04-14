from django.urls import path
from . import views

urlpatterns = [
    path('signOut/', views.signOut, name = 'signOut'),
    path('signIn/', views.signIn, name = 'signIn'),
    path('signIn/signUp/', views.signUp, name = 'signUp'),
    path('detailMyPage/', views.detailMyPage, name = 'detailMyPage'),
    path('detailMyPage/editMyPage/', views.editMyPage, name = 'editMyPage'),
    path('evaluate', views.evaluate, name = 'evaluate'),
]
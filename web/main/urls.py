from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('search/', views.search, name = 'search'),
    path('search/addOrRemove/<str:stockCode>', views.addOrRemove, name = 'addOrRemove'),
]  
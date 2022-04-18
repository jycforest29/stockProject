from django.urls import path
from . import views

urlpatterns = [
    path('detailStockPost/', views.detailStockPost, name = 'detailStockPost'),
]
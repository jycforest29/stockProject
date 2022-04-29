from django.urls import path
from . import views

urlpatterns = [
    path('stockInfo/<str:stockCode>', views.stockInfo, name = 'stockInfo'),
    path('stockInfo/stockAnalysis/<str:stockCode>', views.stockAnalysis, name = 'stockAnalysis'),
    path('stockInfo/stockLike/<str:stockCode>', views.stockLike, name = 'stockLike'),
]  
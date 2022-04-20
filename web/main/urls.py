from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('search/', views.search, name = 'search'),
    path('search/infoStock/<str:stockCode>', views.infoStock, name = 'infoStock'),
    path('search/infoStock/priceStock/<str:stockCode>', views.priceStock, name = 'priceStock'),
    path('search/infoStock/stockLike/<str:stockCode>', views.stockLike, name = 'stockLike'),
] 
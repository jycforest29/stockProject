from django.urls import path
from . import views

urlpatterns = [
    path('modifyStockComment/', views.modifyStockComment, name = 'modifyStockComment'),
    path('writeStockComment/', views.writeStockComment, name = 'writeStockComment'),
]
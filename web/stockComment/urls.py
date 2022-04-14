from django.urls import path
from . import views

urlpatterns = [
    path('modifyComment/', views.modifyComment, name = 'modifyComment'),
    path('writeComment/', views.writeComment, name = 'writeComment'),
    path('delComment/', views.delComment, name = 'delComment'),
]
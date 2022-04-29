from django.urls import path
from . import views

urlpatterns = [
    path('newPost/<str:stockCode>', views.newPost, name = 'newPost'),
    path('detailPost/<int:postPk>', views.detailPost, name = 'detailPost'),
    path('detailPost/reComment/<int:commentPk>/<int:postPk>', views.reComment, name = 'reComment'),
    path('detailPost/likePost/<int:postPk>', views.likePost, name = 'likePost'),
    path('editPost/<int:postPk>', views.editPost, name = 'editPost'),
    path('deletePost/<int:postPk>/<str:stockCode>', views.deletePost, name = 'deletePost'),
] 
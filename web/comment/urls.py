from django.urls import path
from . import views

urlpatterns = [
    path('likeComment/<int:commentPk>', views.likeComment, name = 'likeComment'),
    path('newComment/<int:postPk>', views.newComment, name = 'newComment'),
    path('editComment/<int:commentPk>/<int:postPk>', views.editComment, name = 'editComment'),    
    path('deleteComment/<int:commentPk>/<int:postPk>', views.deleteComment, name = 'deleteComment'),
]
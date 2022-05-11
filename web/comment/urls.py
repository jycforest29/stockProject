from django.urls import path
from . import views

urlpatterns = [
    path('newComment/<int:postPk>', views.newComment, name = 'newComment'),
    path('editComment/<int:commentPk>/<int:postPk>', views.editComment, name = 'editComment'),    
    path('deleteComment/<int:commentPk>/<int:postPk>', views.deleteComment, name = 'deleteComment'),
    path('likeComment/<int:commentPk>', views.likeComment, name = 'likeComment'),
    path('newReComment/<int:postPk>/<int:commentPk>', views.newReComment, name = 'newReComment'),
    path('editReComment/<int:reCommentPk>/<int:postPk>', views.editReComment, name = 'editReComment'),    
    path('deleteReComment/<int:reCommentPk>/<int:postPk>', views.deleteReComment, name = 'deleteReComment'),
    path('likeReComment/<int:reCommentPk>/<int:postPk>', views.likeReComment, name = 'likeReComment'),
]
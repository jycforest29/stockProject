from django.contrib import admin
from .models import Comment

# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'createdAt', 'updatedAt')
    search_fields = ('author', )

admin.site.register(Comment, CommentAdmin)
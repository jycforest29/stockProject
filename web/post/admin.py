from django.contrib import admin
from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('stock', 'author', 'strategy', 'title', 'createdAt', 'updatedAt', 'likeCount', 'commentCount')
    search_fields = ('stock', 'author', 'title')

admin.site.register(Post, PostAdmin)
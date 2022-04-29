from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'strategy']
    def clean(self):
        cleaned_data = super().clean() 
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        strategy = cleaned_data.get('strategy')
        if title and content and strategy:
            return


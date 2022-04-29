from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    def clean(self):
        cleaned_data = super().clean() 
        content = cleaned_data.get('content')
        if content:
            return
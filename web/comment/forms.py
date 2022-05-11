from django import forms
# from .models import Comment

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs = {'class':'cmtCss'}), label = '댓글', max_length=50)
    def clean(self):
        cleaned_data = super().clean() 
        content = cleaned_data.get('content')
        if content:
            return

# 에러체크 수동
class EditForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs = {'class':'cmtCss'}), label = '댓글', max_length=50)

class ReCommentForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs = {'class':'cmtCss'}), label = '대댓글', max_length=50)
    def clean(self):
        cleaned_data = super().clean() 
        content = cleaned_data.get('content')
        if content:
            return 
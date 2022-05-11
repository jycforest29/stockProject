from django import forms
from .models import Post

strategyType = [
        ('매수', '매수'),
        ('중립', '중립'),
        ('매도', '매도'), 
    ]

class PostForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs = {'class':'titleCss'}), label = '제목', max_length=50)
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'contentCss', 'cols':30, 'rows':11}), label = '내용')
    strategy = forms.ChoiceField(widget=forms.Select(), choices=strategyType, label = '의견')


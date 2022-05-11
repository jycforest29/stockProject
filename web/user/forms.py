from django import forms
from .models import User
from django.contrib.auth.hashers import check_password, make_password

strategyType = [
        ("안전형", "안전형"),
        ("중립형", "중립형"), 
        ("위험형", "위험형")
    ]

class SignUpForm(forms.Form):   
    username = forms.CharField(widget=forms.TextInput, max_length = 11, label = '아이디')
    password1 = forms.CharField(widget = forms.PasswordInput,  label = '비밀번호')
    password2 = forms.CharField(widget = forms.PasswordInput,  label = '비밀번호 확인')
    email = forms.EmailField(widget=forms.EmailInput,label = '이메일')
    strategy = forms.ChoiceField(widget=forms.Select(), choices=strategyType, label = '투자 전략 타입')

    def clean(self):
        cleaned_data = super().clean() 
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        strategy = cleaned_data.get('strategy')
        if username and password1 and password2 and email and strategy: 
            user = User.objects.filter(username = username).first()
            userByEmail = User.objects.filter(email = email).first()
            if user is None:
                if userByEmail is None:
                    if check_password(password1, make_password(password2)):
                        return 
                    else:
                        self.add_error('password2', '비밀번호 확인이 비밀번호와 다름')
                else:
                    self.add_error('email', '이미 가입된 이메일임')        
            else:
                self.add_error('username', '이미 존재하는 아이디임')

class SignInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput,max_length = 11, label = '아이디')
    password = forms.CharField(widget = forms.PasswordInput,  label = '비밀번호')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = User.objects.filter(username = username).first()
            if user is not None:
                if check_password(password, user.password):
                    return
                else:
                    self.add_error('username', '비밀번호 다름')
            else:
                self.add_error('password', '아이디 존재하지 않음')


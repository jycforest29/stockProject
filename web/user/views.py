from tempfile import TemporaryFile
from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm, MyPageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import User
from stock.models import Stock

# Create your views here.

def signUp(request):
    form = SignUpForm() 
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            strategy = form.cleaned_data['strategy']
            user = User(username = username, password = make_password(password1), email = email, strategy = strategy)
            user.save()
            login(request, user)
            return redirect('index')
    return render(request, 'user/signUp.html', {'form':form})

def signIn(request): 
    form = SignInForm() 
    if request.method == 'POST':
        # user = authenticate(request, username = username, password = password)
        # if user is not None:
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username = username)
            login(request, user)
            return redirect('index')
    return render(request, 'user/signIn.html', {'form':form})

def signOut(request):
    logout(request)
    messages.success(request, '로그아웃 완료')
    return redirect('index')

def detailMyPage(request):
    return render(request, 'user/detailMyPage.html')

def editMyPage(request):
    myPageForm = MyPageForm()
    if request.method == 'POST':
        myPageForm = MyPageForm(request.POST)
        if myPageForm.is_valid():
            username = request.user.username
            request.user.password = make_password(myPageForm.cleaned_data['password1']) 
            request.user.email = myPageForm.cleaned_data['email']
            request.user.strategy = myPageForm.cleaned_data['strategy']
            # 자동 로그아웃 됨
            request.user.save()
            user = User.objects.get(username = username)
            login(request, user)
            return redirect('detailMyPage')
    return render(request, 'user/editMyPage.html', {'myPageForm':myPageForm})

def evaluate(request):
    return render(request, 'user/evaluate.html')

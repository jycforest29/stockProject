from tempfile import TemporaryFile
from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
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
        # username = request.POST['username']
        # password = request.POST['password']
        # try:
        #     user = User.objects.get(username = username)
        # except:
        #     messages.error(request, '일치하는 회원정보 없음')
        # user = authenticate(request, username = username, password = password)
        # if user is not None:
        #     login(request, user)
        #     return redirect('index')
        # else:
        #     messages.error(request, '비번이 다름')
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

# 유저 정보, 좋아요 누른 주식 정보 제공
def detailMyPage(request):
    likeStockList = Stock.objects.filter(likeUsers__in = [request.user]).order_by('likeCount')
    return render(request, 'user/detailMyPage.html', {'likeStockList':likeStockList})

# 유저 정보, 좋아요 누른 주식 정보 수정 가능
def editMyPage(request):
    return render(request, 'user/editMyPage.html')

# 포트폴리오 평가
def evaluate(request):
    return render(request, 'user/evaluate.html')

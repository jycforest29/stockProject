from tempfile import TemporaryFile
from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import User
from stock.models import Stock
from django.views.decorators.cache import cache_control

# Create your views here.
highStocks = []
midStocks = []
lowStocks = []
# 사용자가 좋아요한 주식별 타유저들의 타입을 분류해서 반환 - 처음 로그인 했을 때
def findStockType(likes):
    global highStocks, midStocks, lowStocks
    high = []
    mid = []
    low = []
    typeList = [high, mid, low]

    for i in likes:
        highNum = 0
        midNum = 0
        lowNum = 0        
        if i.likeUsers.all() is not None:
            for j in i.likeUsers.all():
                if j.strategy == '위험형':
                    highNum += 1 
                elif j.strategy == '중립형':
                    midNum += 1
                else:
                    lowNum += 1    
            typeNum = [highNum, midNum, lowNum]
            typeList[typeNum.index(max(typeNum))].append(i)   
    # return high, mid, low
    
    highStocks = high
    midStocks = mid
    lowStocks = low
    
@cache_control(no_cache = True, must_revalidate = True)
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
            likeStocks = Stock.objects.filter(likeUsers__in = [request.user.pk]).order_by('likeCount')            
            findStockType(likeStocks)
            return redirect('index')
    return render(request, 'user/signUp.html', {'form':form})

@cache_control(no_cache = True, must_revalidate = True)
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
            likeStocks = Stock.objects.filter(likeUsers__in = [request.user.pk]).order_by('likeCount')            
            findStockType(likeStocks)
            return redirect('index')
            
    return render(request, 'user/signIn.html', {'form':form})

@cache_control(no_cache = True, must_revalidate = True)
def signOut(request):
    logout(request)
    messages.success(request, '로그아웃 완료')
    return redirect('index')

def detailMyPage(request):
    return render(request, 'user/detailMyPage.html') 

@cache_control(no_cache = True, must_revalidate = True)
def editMyPage(request):
    if request.method == 'POST':
        pk = request.user.pk
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == '' or password2 == '':
            error = '비밀번호와 비밀번호 확인을 모두 입력하세요'
            return render(request, 'user/editMyPage.html', {'error':error})
        elif password1 != password2:
            error = '비밀번호와 비밀번호 확인이 다름'
            return render(request, 'user/editMyPage.html', {'error':error})
        email = request.POST.get('email')
        strategy = request.POST.get('strategy')
        request.user.password = make_password(password1)
        request.user.email = email
        request.user.strategy = strategy
        # 자동 로그아웃 됨
        request.user.save()        
        user = User.objects.get(pk = pk)
        login(request, user)
        return redirect('detailMyPage')
    else:
        return render(request, 'user/editMyPage.html')

def evaluate(request):
    return render(request, 'user/evaluate.html')

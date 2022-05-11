from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from .models import User
from stock.models import Stock
from django.views.decorators.cache import cache_control
import datetime as dt
import yfinance as yf

# Create your views here.

# <유저가 좋아요한 주식별 각 어떤 타입의 유저가 많이 선택했는지 반환하는 변수>
highStocks = []
midStocks = []
lowStocks = []
kospiResult = 0
kospiIdxValue = 0
start = dt.date.today()
startMid = dt.date.today()
endMid = dt.date.today()
end = dt.date.today()

def likeIdxValue(arg1, start, startMid, endMid, end):
    result = []
    for i in range(len(arg1)):
        tmp = []
        tmpBefore = yf.download(arg1[i].stockCode+'.KS', start = start, end = startMid)['Adj Close']
        tmpAfter = yf.download(arg1[i].stockCode+'.KS', start = endMid, end = end)['Adj Close']
        tmpResult = round( 100*(tmpAfter[0] - tmpBefore[0])/tmpBefore[0] , 2)
        tmp.extend([arg1[i], tmpResult])
        result.append(tmp)   
    return result

# <좋아요한 주식들이 전날과 비교해 코스피 대비 얼마나 변화가 있었는지 나타내는 함수>
def likeStockAnalysis(high, mid, low): 
    global highStocks, midStocks, lowStocks, kospiResult, kospiIdxValue, start, startMid, endMid, end
    
    i = 1
    start = dt.date.today()-dt.timedelta(days = i+1)
    startMid = dt.date.today()-dt.timedelta(days = i)
    endMid = dt.date.today()-dt.timedelta(days = i)
    end = dt.date.today()-dt.timedelta(days = (i-1))
    
    # 현재 날짜로부터 yf로부터 주가 데이터를 갖고올 수 있는 가장 빠른 날짜와 그 다음 빠른 날짜를 찾음
    while True:
        kospiBefore = yf.download('^KS11', start = start, end = startMid)['Adj Close']
        kospiAfter = yf.download('^KS11', start = endMid, end = end)['Adj Close']
        if kospiBefore.size != 0 and kospiAfter.size != 0:
            break
        else:
            # 공휴일이나 주말이 끼어있을 때
            if kospiBefore.size == 0 and kospiAfter.size != 0:
                start = dt.date.today()-dt.timedelta(days = i+1)
                startMid = dt.date.today()-dt.timedelta(days = i)                
            else:
                start = dt.date.today()-dt.timedelta(days = i+1)
                startMid = dt.date.today()-dt.timedelta(days = i)
                endMid = dt.date.today()-dt.timedelta(days = i)
                end = dt.date.today()-dt.timedelta(days = (i-1))
            i += 1
    
    # 각 날짜들에 맞는 데이터 다운로드, 전날 대비 상승/하락 정도와 변화폭으로 배열 값 수정    
    kospiIdxValue = round(kospiAfter[0] - kospiBefore[0], 3)
    kospiResult = round(100*(kospiAfter[0] - kospiBefore[0])/(kospiBefore[0]), 2)    
    
    highStocks = likeIdxValue(high, start, startMid, endMid, end)
    midStocks = likeIdxValue(mid, start, startMid, endMid, end)
    lowStocks = likeIdxValue(low, start, startMid, endMid, end)
    
    # 데이터 시각화
    # fig = plt.figure(figsize=[11, 5])
    # plt.hlines(kospiResult, xmin = 0.0, xmax = 1.0)
    # plt.xlim(0.0, 1.0)
    # plt.ylim(-100, 100)
    # j = 0
    # for i in range(len(likesResult)):
    #     j += 0.9/len(likesResult)
    #     if likesResult[i] < 0:
    #         plt.scatter(j, likesResult[i], c = "blue")
    #     elif likesResult[i] > 0:
    #         plt.scatter(j, likesResult[i], c = "red")
    #     else: 
    #         plt.scatter(j, likesResult[i], c = "cyan")
    #     plt.annotate(text = likesName[i]+'('+str(likesResult[i])+'%'+')', xy = (j, likesResult[i]))    
    # plt.ylabel('%')
    # plt.legend()
    # plt.savefig("likeStockAnalysis.png", dpi = 300)

# <유자가 좋아요한 주식별 타유저들의 타입을 분류해서 반환 - 처음 로그인시, 좋아요한 주식 종목에 변화 있을시 호출>
def findStockType(likes):    
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
    likeStockAnalysis(high, mid, low)

# 폼 활용
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
            return redirect('index')
    return render(request, 'user/signUp.html', {'form':form})

# 폼 활용
@cache_control(no_cache = True, must_revalidate = True)
def signIn(request): 
    form = SignInForm() 
    if request.method == 'POST':
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
    global highStocks, midStocks, lowStocks, kospiResult, kospiIdxValue, start, startMid, endMid, end
    logout(request)

    # 변수 초기화
    highStocks = []
    midStocks = []
    lowStocks = []    
    
    return redirect('index')

def detailMyPage(request):
    return render(request, 'user/detailMyPage.html') 

# 폼 활용하지 않음
@cache_control(no_cache = True, must_revalidate = True)
def editMyPage(request):
    if request.method == 'POST':
        pk = request.user.pk
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == '' or password2 == '' or email == '':
            error = '빈칸 없이 모두 입력해야함'
            return render(request, 'user/editMyPage.html', {'error':error})
        elif password1 != password2:
            error = '비밀번호와 비밀번호 확인이 다름'
            return render(request, 'user/editMyPage.html', {'error':error})
        
        strategy = request.POST.get('strategy')
        request.user.password = make_password(password1)
        request.user.email = email
        request.user.strategy = strategy
        # 자동 로그아웃 됨
        request.user.save()        
        user = User.objects.get(pk = pk)
        login(request, user)
        likeStocks = Stock.objects.filter(likeUsers__in = [request.user.pk]).order_by('likeCount')            
        findStockType(likeStocks)
        return redirect('detailMyPage')
    else:
        return render(request, 'user/editMyPage.html')

def evaluate(request):
    return render(request, 'user/evaluate.html')

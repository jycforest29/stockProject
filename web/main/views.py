from django.http import Http404
from django.shortcuts import render
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from stock.models import Stock
from post.models import Post
from django.db.models import Q
import mpld3
import datetime as dt
from sklearn import preprocessing
from stock.views import searchTop5
# 실검-하루지나면 초기화/이메일 인증/포트폴리오(미완)/애널리스트 분석도 같이 그래프에 넣기/글 댓글 수정
# js - 대댓글/팝업/검색어 자동완성/뒤로가기 버튼/페이징
searchTop5 = searchTop5
# ipoDate를 date 형식으로 db에 저장하기 위해 형식 변환
def setDateFormat(ipoDate):
    return ipoDate.replace('/', '-', 2)

# krx에서 다운받은 한국 주식 정보를 db에 저장(프로그램 초기 실행 한번만 호출)
def initSetting():
    df = pd.read_csv('src/krStock.csv', encoding='cp949')
    for i in range(df.shape[0]):
        Stock.objects.create(
            stockCode = df.loc[i][1],
            stockName = df.loc[i][2],
            ipoDate = setDateFormat(df.loc[i][5]),
            kospi = df.loc[i][6],
            perValue = df.loc[i][10],
            stockNum = df.loc[i][11]
        )

# 주식 검색(종목명, 종목 코드로 검색 가능)
def search(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        searchResults = Stock.objects.filter(Q(stockName__icontains=keyword)|Q(stockCode__icontains=keyword))
        return render(request, 'main/search.html', {'keyword':keyword, 'searchResults':searchResults})
    else:
        raise Http404('검색 엔진 메서드 에러')

# 사용자가 좋아요한 주식별 타유저들의 타입을 분류해서 반환
def findStockType(likes):
    high = []
    mid = []
    low = []
    typeList = [high, mid, low]
    # 쿼리셋은 for문으로 접근 가능
    
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
    return high, mid, low

# 좋아요한 주식들이 전날과 비교해 코스피 대비 얼마나 변화가 있었는지 나타내는 함수
def likeStockAnalysis(likes):
    i = 1
    kospi = 0
    likesResult = []
    likesBefore = []
    likesAfter = []
    likesName = []

    # 현재 날짜로부터 yf로부터 주가 데이터를 갖고올 수 있는 가장 빠른 날짜와 그 전날 날짜를 찾음(주말 제외 포함)
    while True:
        # /목금월/금월화 케이스 고려 안됨
        start = dt.date.today()-dt.timedelta(days = i+2)
        mid = dt.date.today()-dt.timedelta(days = i+1)
        end = dt.date.today()-dt.timedelta(days = i)
        kospiBefore = yf.download('^KS11', start = start, end = mid)['Adj Close']
        kospiAfter = yf.download('^KS11', start = mid, end = end)['Adj Close']
        if kospiBefore.size != 0 and kospiAfter.size != 0:
            break
        i += 1

    # 각 날짜들에 맞는 데이터 다운로드, 변화 정도로 값 변환
    kospi = 100*round((kospiAfter[0] - kospiBefore.iloc[0])/(kospiBefore[0]), 2)    
    for i in likes:
        likesBefore.append(yf.download(i.stockCode+'.KS', start = start, end = mid)['Adj Close'])
        likesAfter.append(yf.download(i.stockCode+'.KS', start = mid, end = end)['Adj Close'])
        likesName.append(i.stockName)
    for i in range(len(likesAfter)):
        likesResult.append(100*round( (likesAfter[i][0] - likesBefore[i][0])/likesBefore[i][0] , 2))

    # 데이터 시각화
    fig = plt.figure(figsize=[11, 5])
    plt.hlines(kospi, xmin = 0.0, xmax = 1.0)
    plt.xlim(0.0, 1.0)
    plt.ylim(-100, 100)
    j = 0
    for i in range(len(likesResult)):
        j += 0.9/len(likesResult)
        if likesResult[i] < 0:
            plt.scatter(j, likesResult[i], c = "blue")
        elif likesResult[i] > 0:
            plt.scatter(j, likesResult[i], c = "red")
        else: 
            plt.scatter(j, likesResult[i], c = "cyan")
        plt.annotate(text = likesName[i]+'('+str(likesResult[i])+'%'+')', xy = (j, likesResult[i]))    
    plt.ylabel('%')
    plt.legend()
    htmlTmp = mpld3.fig_to_html(fig)
    htmlFile = open("main/templates/main/indexResult.html", "w")
    htmlFile.write(htmlTmp)
    htmlFile.close() 

def index(request):
    # initSetting()
    # recommendations = yf.Ticker('JPM').recommendations
    # recommendations = recommendations.iloc[:, 2]

    # 5분 단위로 검색량이 가장 많은 주식 5개 찾음
    global searchTop5
    topStocks = []
    tmp = []
    tmp = sorted(searchTop5.items(), key = lambda item: item[1], reverse = True)[:5]
    for i in tmp:
        stock = Stock.objects.get(stockName = i[0])
        topStocks.append(stock)
    
    stockRanking = Stock.objects.filter(likeCount__gte = 1).order_by('likeCount')
    likeStocks = None
    if request.user:
        # 왜 pk로 바꾸니까 된거지?
        likeStocks = Stock.objects.filter(likeUsers__in = [request.user.pk]).order_by('likeCount')
        highStocks, midStocks, lowStocks = findStockType(likeStocks)
        # compareToKospiFunc(likeStocks)
    return render(request, 'main/index.html', {'stockRanking':stockRanking, 'highStocks':highStocks,'midStocks':midStocks,'lowStocks':lowStocks, 'topStocks':topStocks}) 
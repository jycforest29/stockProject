from sched import scheduler
from django.http import Http404
from django.shortcuts import render, redirect
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from stock.models import Stock
from post.models import Post
from django.db.models import Q
import mpld3
import datetime as dt
from sklearn import preprocessing
from user.views import findStockType
from apscheduler.schedulers.background import BackgroundScheduler
from django.views.decorators.cache import cache_control

searchRanking = []
likeRanking = []
keyword = ''
pltTag = None


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

def per5min():
    from stock.views import searchTop5 
    global likeRanking, searchRanking
    
    likeRanking = Stock.objects.filter(likeCount__gte = 1).order_by('likeCount')[:5]
    searchRanking = []
    stocks = sorted(searchTop5.items(), key = lambda item: item[1], reverse = True)[:5]
    for i in stocks:
        stock = Stock.objects.get(stockName = i[0])
        searchRanking.append(stock)
    

# 주식 검색(종목명, 종목 코드로 검색 가능)
def search(request):
    global keyword
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        searchResults = Stock.objects.filter(Q(stockName__icontains=keyword)|Q(stockCode__icontains=keyword))
        return render(request, 'main/search.html', {'keyword':keyword, 'searchResults':searchResults})
    else:
        raise Http404('검색 엔진 메서드 에러')

# def like(user, stockCode):
#     stock = Stock.objects.get(stockCode = stockCode)
#     if user in stock.likeUsers.all():
#         stock.likeUsers.remove(user)
#         stock.likeCount -= 1
#     else:
#         stock.likeUsers.add(user)
#         stock.likeCount += 1    
#     stock.save()    

@cache_control(no_cache = True, must_revalidate = True)
def addOrRemove(request, stockCode):    
    stock = Stock.objects.get(stockCode = stockCode)
    if request.user in stock.likeUsers.all():
        stock.likeUsers.remove(request.user)
        stock.likeCount -= 1
    else:
        stock.likeUsers.add(request.user)
        stock.likeCount += 1    
    stock.save()    
    likeStocks = Stock.objects.filter(likeUsers__in = [request.user.pk]).order_by('likeCount')  
    findStockType(likeStocks)
    
    kw = keyword
    searchResults = Stock.objects.filter(Q(stockName__icontains=kw)|Q(stockCode__icontains=kw))
    return render(request, 'main/search.html', {'keyword':kw, 'searchResults':searchResults})


# 좋아요한 주식들이 전날과 비교해 코스피 대비 얼마나 변화가 있었는지 나타내는 함수
def likeStockAnalysis(likes):
    global pltTag
    i = 1
    kospi = 0
    likesResult = []
    likesBefore = []
    likesAfter = []
    likesName = []
    
    start = dt.date.today()-dt.timedelta(days = i+1)
    startMid = dt.date.today()-dt.timedelta(days = i)
    endMid = dt.date.today()-dt.timedelta(days = i)
    end = dt.date.today()-dt.timedelta(days = (i-1))
    # 현재 날짜로부터 yf로부터 주가 데이터를 갖고올 수 있는 가장 빠른 날짜와 그 전날 날짜를 찾음(주말 제외 포함)
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
    
    # 각 날짜들에 맞는 데이터 다운로드, 변화 정도로 값 변환
    kospi = 100*round((kospiAfter[0] - kospiBefore.iloc[0])/(kospiBefore[0]), 2)    
    for i in likes:
        likesBefore.append(yf.download(i.stockCode+'.KS', start = start, end = startMid)['Adj Close'])
        likesAfter.append(yf.download(i.stockCode+'.KS', start = endMid, end = end)['Adj Close'])
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
    pltTag = mpld3.fig_to_html(fig)
    htmlFile = open("main/templates/main/likeStockAnalysis.html", "w")
    htmlFile.write(pltTag)
    htmlFile.close() 

    
def index(request):
    # initSetting()
    from user.views import highStocks, midStocks, lowStocks
    likeStocks = Stock.objects.filter(likeUsers__in = [request.user.pk]).order_by('likeCount')
    
    sched = BackgroundScheduler()
    sched.add_job(per5min, 'interval', minutes = 5, id = 'per5min')
    sched.start()
    # likeStockAnalysis(likeStocks)
    # pltTagTmp = '''<DOCTYPE html><html><head><meta charset = "utf-8"></head><body>'''+pltTag+'''</body></html>'''
    # print(pltTag) 
    # schedule.every(30).seconds.do(per30min)
    # while True:
    #     per30min()
    #     time.sleep(60)
    
    return render(request, 'main/index.html', {'likeRanking':likeRanking, 'highStocks':highStocks,'midStocks':midStocks,'lowStocks':lowStocks, 'searchRanking':searchRanking, 'pltTag':pltTag}) 

from django.http import Http404
from django.shortcuts import render, redirect
import pandas as pd
from stock.models import Stock
from django.db.models import Q
from apscheduler.schedulers.background import BackgroundScheduler
from django.views.decorators.cache import cache_control
from user.views import findStockType

# 조회량 상위 5개 주식 
searchRanking = []
# 좋아요 상위 5개 주식 
likeRanking = []
# 처음 index.html 로딩됐을 때 per5min함수 호출하기 위한 변수
per5minStart = False
keyword = ''

# <src/krStock.csv 파일을 mysql에 저장>
# initSetting 함수에서 ipoDate를 date 형식으로 db에 저장하기 위해 형식 변환
def setDateFormat(ipoDate):
    return ipoDate.replace('/', '-', 2)
# krx에서 다운받은 한국 주식 정보를 db에 저장
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

# <5분에 한번씩 likeRanking, searchRanking 변수값 갱신>
def per5min():
    from stock.views import searchCount
    global likeRanking, searchRanking
    
    likeRanking = Stock.objects.filter(likeCount__gte = 1).order_by('likeCount')[:5]
    searchRanking = []
    stocks = sorted(searchCount.items(), key = lambda item: item[1], reverse = True)[:5]
    for i in stocks:
        stock = Stock.objects.get(stockName = i[0])
        searchRanking.append(stock)

# <주식 검색(종목명, 종목 코드로 검색 가능)>
def search(request):
    global keyword
    if request.method == 'GET':
        if request.GET.get('keyword') == None:
            keyword = keyword
        else:
            keyword = request.GET.get('keyword')
        searchResults = Stock.objects.filter(Q(stockName__icontains=keyword)|Q(stockCode__icontains=keyword))
        return render(request, 'main/search.html', {'keyword':keyword, 'searchResults':searchResults})
    else:
        raise Http404('검색 엔진 메서드 에러')

# <stockInfo.html말고 search.html에서 주식 좋아요에 추가/제거>
# 뒤로가기 제어 데코레이터
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
    # index.html의 '유저가 좋아요한 주식'항목에 반영사항 업데이트
    likeStocks = Stock.objects.filter(likeUsers__in = [request.user.pk]).order_by('likeCount')  
    findStockType(likeStocks)
    return redirect('search')

def index(request):
    global per5minStart, keyword
    # initSetting()
    from user.views import highStocks, midStocks, lowStocks, kospiResult, kospiIdxValue, start, startMid, endMid, end
    # 전역변수 초기화
    keyword = ''
    if per5minStart == False:
        per5min()
        per5minStart = True
    sched = BackgroundScheduler()
    sched.add_job(per5min, 'interval', minutes = 5, id = 'per5min')
    sched.start()
    
    return render(request, 'main/index.html', {'likeRanking':likeRanking, 'highStocks':highStocks,'midStocks':midStocks,'lowStocks':lowStocks, 'searchRanking':searchRanking, 'kospiResult':kospiResult, 'kospiIdxValue':kospiIdxValue, 'start':start, 'startMid':startMid, 'endMid':endMid, 'end':end}) 

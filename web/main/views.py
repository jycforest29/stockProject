from django.http import Http404
from django.shortcuts import render, redirect
from numpy import index_exp
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date, datetime
from stock.models import Stock
from django.db.models import Q
import math
import numpy as np
import mpld3
import datetime as dt
from sklearn import preprocessing
from user.models import User

# 글, 댓글 - 글은 해당 주식, 주식에 대한 의견 / 각 주식별 인기글 - index.html에 많으면 ->으로 넘기기 / 글, 댓글 모두 유저 타입 보여주기, 각 글과 댓글별 퍼센트 보여주기
# 유저 마이페이지, 마이페이지 수정 완성, 포트폴리오 - 평균 수익(각 타입의 유저별 평균 수익은 이렇다)
# 그래프들 js로 팝업 띄우기/ 애널리스트 분석도 같이 그래프에 넣기

buyType = ['Buy', 'Outperform',  'Overweight']
holdType = ['Hold', 'Neutral', 'Market Perform', 'Sector Perform', 'Peer Perform']
sellType = ['Sell', 'Underperform']
idxList = []
idxName = []

def setDateFormat(ipoDate):
    return ipoDate.replace('/', '-', 2)

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

def search(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        searchResults = Stock.objects.filter(Q(stockName__icontains=keyword)|Q(stockCode__icontains=keyword))
        return render(request, 'main/search.html', {'keyword':keyword, 'searchResults':searchResults})
    else:
        raise Http404('검색 엔진 메서드 에러')

# df로 합치고 0 제거
def removeZeroData(*s):    
    df = pd.DataFrame()
    for i in range(len(s)):
        df['s'+str(i)] = s[i]

    df = df.loc[df.s1 !=0]
    # df = df.drop(index=df.loc[df.s2 == 0].index) 
    return df

# df -> tmp안의 시리즈 배열 -> 각 시리즈를 df로 변환, 데이터 전처리 후 이 배열 리턴
def arrangeIndexData(df):
    tmp = []        
    maxAbsScaler = preprocessing.MaxAbsScaler()

    for i in range(df.shape[1]):
        tmp.append(df['s'+str(i)])
        # df[:, i] = minMaxScaler.fit_transform(df[:, i])

    # print(type(tmp[i])) => 시리즈
    # df
    for i in range(len(tmp)):
        dfTmp = pd.DataFrame(tmp[i])
        # s0등 존재
        # print(dfTmp)
        tmp[i] = maxAbsScaler.fit_transform(dfTmp)
    # array
    # print(tmp)
    # for i in range(df.shape[1]):
    #     tmp.append(df.iloc[:, i])
    return tmp

# /데이터 정제
def returnRecommendation(stockCode):
    recommendations = yf.Ticker(stockCode).recommendations
    return recommendations

def indexAnalysis(checkbox, stockCode, start):
    global idxList, idxName    
    priceTmp = yf.download(stockCode+'.KS', start = start)[['Adj Close', 'Volume']]
    kospi = yf.download('^KS11', start = start)['Adj Close']
    adjClose = priceTmp['Adj Close']
    volume = priceTmp['Volume']

    idxList = arrangeIndexData(removeZeroData(adjClose, volume, kospi))
    idxName = ['adj' ,'vol', 'kospi']

    idxListTmp = idxList[:]
    idxNameTmp = idxName[:]

    i = 0
    j = 0
    while i < 3:
        if checkbox[j] == None:
            del idxListTmp[j]
            del idxNameTmp[j]
        else:
            j += 1
        i += 1
    
    recommendations = returnRecommendation(stockCode)   

    # /팝업창으로 띄우기
    fig = plt.figure()
    for i in idxListTmp:
        plt.plot(i)
    plt.xlabel('date')
    plt.ylabel('index')
    plt.legend()
    htmlTmp = mpld3.fig_to_html(fig)
    htmlFile = open("main/templates/main/indexResult.html", "w")
    htmlFile.write(htmlTmp)
    htmlFile.close()
    
    idxListTmp = idxList
    idxNameTmp = idxName

def priceStock(request, stockCode):    
    if request.method == 'POST':
        start = request.POST.get('start')
        checkbox1 = request.POST.get('checkbox1')
        checkbox2 = request.POST.get('checkbox2')
        checkbox3 = request.POST.get('checkbox3')
        indexAnalysis([checkbox1, checkbox2, checkbox3], stockCode, start)
        return render(request, 'main/indexResult.html')
    else:
        raise Http404('가격 조회 메서드 에러')

def infoStock(request, stockCode):
    stockData = Stock.objects.get(stockCode = stockCode)
    startDate = stockData.ipoDate.strftime("%Y-%m-%d")
    endDate = (dt.date.today()-dt.timedelta(days = 1)).strftime("%Y-%m-%d")
    userInStock = False
    if request.user in stockData.likeUsers.all():
        userInStock = True

    # /관련 종목 게시판 글
    return render(request, 'main/infoStock.html', {'stockData':stockData, 'startDate':startDate, 'endDate':endDate, 'userInStock':userInStock})

def stockLike(request, stockCode):
    stock = Stock.objects.get(stockCode = stockCode)
    if request.user in stock.likeUsers.all():
        stock.likeUsers.remove(request.user)
        stock.likeCount -= 1
    else:
        stock.likeUsers.add(request.user)
        stock.likeCount += 1
    stock.save()
    return redirect('infoStock', stockCode)

def compareToKospiFunc(likeStocks):
    i = 1
    kospiList = []
    likeStocksList = []
    likeStocksBefore = []
    likeStocksAfter = []
    likeResult = []

    while True:
        # 목금월/금월화 케이스 고려 안됨
        start = dt.date.today()-dt.timedelta(days = i+2)
        mid = dt.date.today()-dt.timedelta(days = i+1)
        end = dt.date.today()-dt.timedelta(days = i)
        kospiBefore = yf.download('^KS11', start = start, end = mid)['Adj Close']
        kospiAfter = yf.download('^KS11', start = mid, end = end)['Adj Close']
        if kospiBefore.size and kospiAfter.size != 0:
            break
        i += 1
    
    for i in likeStocks:
        likeStocksBefore.append(yf.download(i.stockCode+'.KS', start = start, end = mid)['Adj Close'])
        likeStocksAfter.append(yf.download(i.stockCode+'.KS', start = mid, end = end)['Adj Close'])

    maxAbsScaler = preprocessing.MaxAbsScaler()
    # df = pd.DataFrame()
    # # Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample.
    # df['s0'] = kospi
    # for i in range(1, len(likeStocksTmp)):
    #     df['s'+str(i)] = likeStocksTmp[i-1]
    # # likeResult = [0, 1, 2, 3,4 ,5]
    # fig = plt.figure()
    # plt.plot(df[['s0']])
    # # j = 0.00
    # # for i in range(1, len(likeResult)):
    # #     j += 0.1//len(likeResult)
    # #     plt.scatter(j, likeResult[i])
    # plt.ylabel('index')
    # plt.legend()
    # htmlTmp = mpld3.fig_to_html(fig)
    # htmlFile = open("main/templates/main/index.html", "a")
    # htmlFile.write(htmlTmp)
    # htmlFile.close()

# def checkColumnValue(df):
#     global buyType, sellType
#     # ['', 'Buy', 'Hold', 'Neutral', 'Outperform', 'Underperform', 'Market Perform', 'Sector Perform', 'Sell', 'Overweight', 'Peer Perform']
#     tmp = []
#     for i in range(df.shape[0]):
#         if df[i] not in tmp:
#             tmp.append(df[i])


# Create your views here.
def index(request):
    # initSetting()
    # recommendations = yf.Ticker('JPM').recommendations
    # recommendations = recommendations.iloc[:, 2]
    stockRanking = Stock.objects.filter(likeCount__gte = 1).order_by('likeCount')
    # allowed field?
    likeStocks = None
    if request.user:
        likeStocks = Stock.objects.filter(likeUsers__in = [request.user]).order_by('likeCount')
        compareToKospiFunc(likeStocks)
    # checkColumnValue(recommendations)   
    return render(request, 'main/index.html', {'stockRanking':stockRanking, 'likeStocks':likeStocks})
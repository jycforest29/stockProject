from django.http import Http404
from django.shortcuts import render
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

# 액면가가 무액면이거나 1 이하일 경우 0으로 데이터 전처리 -> 그대로 나타내야(모델 필드 수정)
def checkPerValue(perValue):
    try:
        int(perValue) > 1
        return perValue
    except:
        return 0

def initSetting():
    df = pd.read_csv('src/krStock.csv', encoding='cp949')
    for i in range(df.shape[0]):
        Stock.objects.create(
            stockCode = df.loc[i][1],
            stockName = df.loc[i][2],
            ipoDate = df.loc[i][5],
            kospi = df.loc[i][6],
            perValue = checkPerValue(df.loc[i][10]),
            stockNum = df.loc[i][11]
        )

def search(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        searchResults = Stock.objects.filter(Q(stockName__icontains=keyword)|Q(stockCode__icontains=keyword))
        return render(request, 'main/search.html', {'keyword':keyword, 'searchResults':searchResults})
    else:
        raise Http404('검색 엔진 메서드 에러')

# 코스피값으로 통일
def arrangeIndexData(adjClose, volume, kospi):
    volume = volume.astype(np.float64)
    indexData = [adjClose, volume, kospi]
    indexData.sort(key = lambda x: int(math.log10(int(max(x)))))
    minNum = int(math.log10(int(max(indexData[0]))))
    minLen = min(indexData, key = lambda x: x.shape[0]).shape[0]
    for i in range(1, len(indexData)):
        now = int(math.log10(int(indexData[i][0])))
        for j in range(minLen):
            try:              
                indexData[i][j] /= math.pow(10, (now-minNum))
            except:      
                pass
    return adjClose, volume, kospi

def priceStock(request, stockCode):
    stockData = Stock.objects.get(stockCode = stockCode)
    if request.method == 'POST':
        # 선택 날짜 받아오기(상장일부터)
        start = request.POST.get('start')
        # 애널리스트 데이터 있으면 받아오기
        priceTmp = yf.download(stockCode+'.KS', start = start)[['Adj Close', 'Volume']]
        kospi = yf.download('^KS11', start = start)['Adj Close']

        adjClose, volume, kospi = arrangeIndexData(priceTmp['Adj Close'] , priceTmp['Volume'], kospi)

        # 웹에 올리기
        # fig = plt.figure()
        # plt.plot(adjClose, label = 'adj')
        # plt.plot(volume, label = 'volume')
        # plt.plot(kospi, label = 'kospi')
        # plt.legend()
        # htmlTmp = mpld3.fig_to_html(fig)
        # htmlFile = open("main/templates/main/index.html", "a")
        # htmlFile.write(htmlTmp)
        # htmlFile.close()

        return render(request, 'main/infoStock.html', {'stockData':stockData})
    else:
        raise Http404('가격 조회 메서드 에러')

def infoStock(request, stockCode):
    stockData = Stock.objects.get(stockCode = stockCode)
    # /분석 종류 js
    # /관련 종목 게시판 글
    return render(request, 'main/infoStock.html', {'stockData':stockData})

# 좋아요
def stockLike(request, stockCode):
    # stock = Stock.Objects.get(stockCode = stockCode)
    # if request.user in stock.likeUsers.all():
    #     stock.likeUsers.remove(request.user)
    # else:
    #     stock.likeUsers.add(request.user)
    return render(request, 'main/infoStock.html')

def compareToKospiFunc(likeStocks):
    # 좋아요한 그래프 - 상수함수와 점들
    yesterday = dt.date.today()-dt.timedelta(day = 1)
    kospi = yf.download('^KS11', start = yesterday)['Adj Close']
    likeStocksTmp = []
    for i in likeStocks:
        likeStocksTmp.append(yf.download(i.stockCode+'.KS', start = yesterday)['Adj Close'])
    return 0

# Create your views here.
def index(request):
    # initSetting()
    # likeStokcs = []
    # compareToKospiFunc
    return render(request, 'main/index.html')

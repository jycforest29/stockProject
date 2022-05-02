from django.shortcuts import render, redirect
from django.http import Http404
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from stock.models import Stock
from post.models import Post
import numpy as np
import mpld3
import datetime as dt
from sklearn import preprocessing

# Create your views here.

# 애널리스트 의견별 분류
buyType = ['Buy', 'Outperform',  'Overweight']
holdType = ['Hold', 'Neutral', 'Market Perform', 'Sector Perform', 'Peer Perform']
sellType = ['Sell', 'Underperform']

# 거래량, 종가, 코스피 지수 항목에 대한 리스트
checkIdx = []
checkName = ['adj' ,'vol', 'kospi']

searchTop5 = {}
# 0인 데이터 제거, 시리즈의 value값 수정
def arrangeIndexData(*s):  
    sList = []    

    # 인자로 받은 시리즈들을 하나의 데이터프레임으로 변환
    df = pd.DataFrame()
    for i in range(len(s)):
        df['s'+str(i)] = s[i]

    # 칼럼 중 value가 0인 값이 포함된 날짜의 모든 칼럼별 데이터 제거
    df = df.loc[df.s1 !=0] # df = df.drop(index=df.loc[df.s2 == 0].index) 
    # 시각화 시 필요한 칼럼들 추출
    dates = df['s3']
    adjCloseText = df['s0']
    df = df[['s0', 's1', 's2']]

    # 변환한 데이터프레임을 다시 각각 시리즈로 변환
    for i in range(df.shape[1]):
        sList.append(df['s'+str(i)])
    
    # 거래량 칼럼의 타입을 int에서 float으로 변환
    sList[1] = sList[1].astype('float64')
    for i in range(len(sList)):
        for j in range(sList[i].shape[0]-1):
            # 각 시리즈의 value들을 전날 대비 변한 수치로 수정
            sList[i][j] = (sList[i][j] - sList[i][j+1]) / sList[i][j]
        sList[i] = sList[i][:-1]        
    
    # preprocessData의 인자로 df를 넣기 위해 sList를 다시 df로 변환 
    for i in range(len(sList)):
        df['s'+str(i)] = sList[i]

    return df, dates, adjCloseText

# maxAbsScaler를 통한 데이터 전처리
def preprocessData(df):    
    result = []      
    # df[['s3']] -> df, df['s3'] -> series
    # dates = df['s3']    
    maxAbsScaler = preprocessing.MaxAbsScaler()
    checkArray = maxAbsScaler.fit_transform(df)

    for i in range(df.shape[1]):
        result.append(checkArray[:, i])
    return result

# 그래프에서 선택한 날짜별 당시 애널리스트 의견 데이터 제공
def returnRecommendation(stockCode):
    recommendations = yf.Ticker(stockCode).recommendations
    # recommendations = yf.Ticker('JPM').recommendations
    # recommendations = recommendations.iloc[:, 2]
    return recommendations

# 유저가 체크한 값들(checkbox), 주식(stockCode), 분석 시작 날짜(start)에 따른 주가 데이터 분석
def indexAnalysis(checkbox, stockCode, start):
    global checkIdx, checkName    
    stockIdx = yf.download(stockCode+'.KS', start = start)[['Adj Close', 'Volume']]
    kospiIdx = yf.download('^KS11', start = start)['Adj Close']
    adjClose = stockIdx['Adj Close']
    volume = stockIdx['Volume']
    dates = volume.index.to_frame().iloc[:, 0]
    
    checkIdx, dates, adjCloseText = arrangeIndexData(adjClose, volume, kospiIdx, dates)
    checkIdx = preprocessData(checkIdx)
    
    # 체크박스에 체크된 값만 그래프에 표시
    checkIdxTmp = checkIdx[:]
    checkNameTmp = checkName[:]
    i = 0
    j = 0
    while i < 3:
        if checkbox[j] == None:
            del checkIdxTmp[j]
            del checkNameTmp[j]
        else:
            j += 1
        i += 1
    
    recommendations = returnRecommendation(stockCode)   

    # plot함수에 맞는 타입으로 변경
    dates = dates.to_numpy()
    checkNameTmp = np.array(checkNameTmp)

    # 팝업창으로 띄우기
    fig = plt.figure(figsize=[11, 5])
    for i in range(len(checkIdxTmp)):
        plt.plot(dates, checkIdxTmp[i], label = checkNameTmp[i])
        # plt.text(dates[i], checkIdxTmp[i], 'adj')
    for i in range(len(checkIdxTmp)):
        for j in range(checkIdxTmp[i].shape[0]):
            plt.text(dates[j], checkIdxTmp[i][j], adjCloseText[j])
    plt.xlabel('date')
    plt.ylabel('index')
    plt.legend()
    htmlTmp = mpld3.fig_to_html(fig)
    htmlFile = open("stock/templates/stock/indexResult.html", "w")
    htmlFile.write(htmlTmp)
    htmlFile.close()
    
    checkIdxTmp = checkIdx
    checkNameTmp = checkName

# 지표에 기반한 분석 시작 함수
def stockAnalysis(request, stockCode):    
    if request.method == 'POST':
        start = request.POST.get('start')
        checkbox1 = request.POST.get('checkbox1')
        checkbox2 = request.POST.get('checkbox2')
        checkbox3 = request.POST.get('checkbox3')
        indexAnalysis([checkbox1, checkbox2, checkbox3], stockCode, start)
        return render(request, 'stock/indexResult.html')
    else:
        raise Http404('가격 조회 메서드 에러')

# 검색한 종목의 기본적인 정보 리턴하는 함수
def stockInfo(request, stockCode):
    # 검색량 상위 5개안에 드는 주식들 찾기 위해 stockInfo 페이지 클릭시마다 searchTop5 딕셔너리에 더함
    global searchTop5
    stockData = Stock.objects.get(stockCode = stockCode)
    if stockData.stockName in searchTop5.keys():
        searchTop5[stockData.stockName] += 1
    else:
        searchTop5[stockData.stockName] = 1
    
    # stockInfo.html의 input에 필요한 값들
    startDate = stockData.ipoDate.strftime("%Y-%m-%d")
    endDate = (dt.date.today()-dt.timedelta(days = 1)).strftime("%Y-%m-%d")

    userInStock = False
    if request.user in stockData.likeUsers.all(): 
        userInStock = True
        
    # 해당 주식의 게시글에는 매수/중립/매도의견이 각각 몇 %였는지    
    posts = Post.objects.filter(stock = stockData)    
    postsBuy = posts.filter(strategy = '매수').count()    
    postsHold = posts.filter(strategy = '중립').count()       
    postsSell = posts.filter(strategy = '매도').count()
    postsStrategySum = sum([postsBuy,postsHold,postsSell] )       
    strategyText = '매수: '+ str(0 if postsBuy ==0 else int(postsBuy / postsStrategySum)*100) + ' 중립: '+ str(0 if postsHold ==0 else int(postsHold / postsStrategySum)*100) + ' 매도: '+ str(0 if postsSell ==0 else int(postsSell / postsStrategySum)*100)
    
    topPosts = posts.order_by('-likeCount')[:5]
    return render(request, 'stock/stockInfo.html', {'stockData':stockData, 'startDate':startDate, 'endDate':endDate, 'userInStock':userInStock, 'posts':posts, 'strategyText':strategyText, 'topPosts':topPosts})

# 주식 좋아요
def stockLike(request, stockCode):
    stock = Stock.objects.get(stockCode = stockCode)
    if request.user in stock.likeUsers.all():
        stock.likeUsers.remove(request.user)
        stock.likeCount -= 1
    else:
        stock.likeUsers.add(request.user)
        stock.likeCount += 1    
    stock.save()  
    return redirect('stockInfo', stockCode)

 
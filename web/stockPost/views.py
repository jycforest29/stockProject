from django.shortcuts import render
import yfinance as yf
from matplotlib import pyplot as plt
import pandas as pd

# Create your views here.
# def codeToName(stockCode):

# stockPost.html
# 단위 변환 - 다른 영역에도 적용 : 코스피는 1000단위임, 따라서 거래량/가격 모두 1000단위로 변환 후 변환율 나타내기
# 애널리스트 보고서 있으면 링크 끼워넣기 - analyst detail.html과 연결, 요약(외부 lib 사용)해서 보여주기, +버튼으로 눌러서 누른것들 전부 analyspost로 연결
# 캘린더 - 날짜별(상장이후부터), 분석 요구사항별 - 조회눌러야 같이 조회
# 유사업종 - 주식 데이터 제공 사이트 섹터명 참고
# html에 plt 나타내기 - 파일?

kospiIndex = pd.DataFrame()
keywordIndex = pd.DataFrame()
dataLoaded = False

# 인자는 데이터프레임 형태여야
def convertYlabelUnit(toConvert):
    pass

def load_data(start):
    global kospiIndex, keywordIndex

    kospiIndex = yf.download('^KS11', interval='1d', start = start)['Adj Close']
    keywordIndex = yf.download('005930.KS', interval='1d', start = start)[['Adj Close', 'Volume']]

def detailStockPost(request):
    global dataLoaded
    start = '2019-04-09'
    if not dataLoaded:
        load_data(start)
        dataLoaded = True
    
    plt.subplot(3, 1, 1)
    plt.plot(kospiIndex, label = 'kospi')
    plt.plot(keywordIndex['Adj Close'], label ='adj')
    plt.legend()
    plt.xlabel('kospi')
    plt.ylabel('adj')

    plt.subplot(3, 1, 2)
    plt.plot(kospiIndex, label = 'kospi')
    plt.plot(keywordIndex['Volume'], label = 'volume')
    plt.yscale('linear')

    plt.subplot(3, 1, 3)
    plt.plot(keywordIndex['Adj Close'], label ='adj')
    plt.plot(keywordIndex['Volume'], label = 'volume')
    plt.yscale('log')

    plt.savefig('src/plt_data.png', dpi = 100)

    return render(request, 'stockPost/detailStockPost.html')

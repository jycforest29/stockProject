from django.shortcuts import render
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mpld3

# koreaStock.csv
columnNames = ['단축코드', '한글 종목명', '상장일', '액면가', '상장주식수']
koreaStockDf = pd.read_csv('src/koreaStock.csv', encoding='cp949', usecols = columnNames)

# index.html
# 주식 검색기능 - 단어 포함, 주식 이름으로만 검색 
# 좋아요 한 주식의 코스피 대비 상승폭(어제), 동일 업종 대비 상승폭(평균)
def search():
    pass

# Create your views here.
def index(request):
    return render(request, 'main/index.html') 
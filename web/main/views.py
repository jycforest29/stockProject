from tabnanny import check
from django.http import Http404
from django.shortcuts import render
from numpy import record
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date, datetime
import pymysql
import csv

# index.html
# mysql에 넣기 및 연동 -> search 함수 구현 -> check_start 함수 구현 -> 코스피 대비 상승폭, 동일 업종 대비 상승폭 구현 -> 검색어 자동완성
def csv_to_mysql():
    pass

def search(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
    else:
        raise Http404('검색 엔진 메서드 에러')
    return render(request, 'main/search.html', {'keyword':keyword})

def check_start():
    y = datetime.now().year
    m = datetime.now().month
    d = datetime.now().day-1
    return str(y)+'-'+str(m)+'-'+str(d)

# Create your views here.
def index(request):
    likes = ['005930']
    compare_to_kospi = []
    compare_to_sector = []
    for i in likes:
        compare_to_kospi.append((yf.download(i+'.KS', start = check_start()))['Adj Close'])
    return render(request, 'main/index.html', {'compare_to_kospi':compare_to_kospi, 'compare_to_sector':compare_to_sector}) 
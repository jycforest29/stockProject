from django.shortcuts import render
import yfinance as yf
from matplotlib import pyplot as plt
import pandas as pd

# Create your views here.
# def codeToName(stockCode):


def detailStockPost(request):
    todayData = yf.download('005930.KS', start = '2021-04-14')
    todayData = todayData.to_html()

    file = open("stockPost/templates/stockPost/detailStockPost.html", "w")
    file.write(todayData)
    file.close()
        
    return render(request, 'stockPost/detailStockPost.html')

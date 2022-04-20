from django.shortcuts import render
import yfinance as yf
from matplotlib import pyplot as plt
import pandas as pd

# Create your views here.

def detailPost(request):
    return render(request, 'post/detailPost.html')

from django.shortcuts import render

# Create your views here.

def modifyComment(request):
    return render(request, 'stockPost/detailStockPost.html')

def writeComment(request):
    return render(request, 'stockPost/detailStockPost.html')

def delComment(request):
    return render(request, 'stockPost/detailStockPost.html')
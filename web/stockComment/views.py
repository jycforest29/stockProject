from django.shortcuts import render

# Create your views here.

def modifyStockComment(request):
    return render(request, 'stockComment/modifyStockComment.html')

def writeStockComment(request):
    return render(request, 'stockComment/writeStockComment.html')
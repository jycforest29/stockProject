from django.shortcuts import render

# Create your views here.

def modifyComment(request):
    return render(request, 'post/detailPost.html')

def writeComment(request):
    return render(request, 'post/detailPost.html')

def delComment(request):
    return render(request, 'post/detailPost.html')
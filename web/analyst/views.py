from django.shortcuts import render

# Create your views here.

def analystPost(request):
    return render(request, 'analyst/analystPost.html')
 
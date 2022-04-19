from django.shortcuts import render

# Create your views here.
 
def newsPost(request):
    return render(request, 'news/newsPost.html')

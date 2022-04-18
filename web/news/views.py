from django.shortcuts import render

# Create your views here.
 
def detailNewsPost(request):
    return render(request, 'newsPost/detailNewsPost.html')

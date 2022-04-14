from django.shortcuts import render

# Create your views here.

def signUp(request):
    return render(request, 'user/signUp.html')

def signIn(request):
    return render(request, 'user/signIn.html')

def signOut(request):
    return render(request, 'user/signIn.html')

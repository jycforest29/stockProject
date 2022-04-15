from django.shortcuts import render

# Create your views here.

def signUp(request):
    return render(request, 'user/signUp.html')

def signIn(request):
    return render(request, 'user/signIn.html')

def signOut(request):
    return render(request, 'user/signIn.html')

def detailMyPage(request):
    return render(request, 'user/detailMyPage.html')

def editMyPage(request):
    return render(request, 'user/editMyPage.html')

# evaluate.html
# 좋아요 누른 주식과 그 주식에서 찜한 애널리스트 글 목록(타이틀만), 다른 유저들의 평균 수익률 대비 수익률, 코스피 대비 수익률, stockPost 설정 그대로
def evaluate(request):
    return render(request, 'user/evaluate.html')

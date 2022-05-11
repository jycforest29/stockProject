from django.shortcuts import render, redirect
from .forms import PostForm
from comment.forms import CommentForm, ReCommentForm
from stock.models import Stock
from .models import Post
from comment.models import Comment
from django.http import Http404
from django.utils import timezone
from django.views.decorators.cache import cache_control

# Create your views here.

# 폼 활용
def detailPost(request, postPk): 
    post = Post.objects.get(pk = postPk)
    commentForm = CommentForm()
    reCommentForm = ReCommentForm()    
    comments = Comment.objects.filter(post = post)
    return render(request, 'post/detailPost.html', {'post':post, 'commentForm':commentForm, 'reCommentForm':reCommentForm ,'comments':comments})

# 폼 활용
@cache_control(no_cache = True, must_revalidate = True)
def newPost(request, stockCode):
    postForm = PostForm()
    stock = Stock.objects.get(stockCode = stockCode)
    if request.method == 'POST':
        postForm = PostForm(request.POST)
        if postForm.is_valid():
            title = postForm.cleaned_data['title']
            content = postForm.cleaned_data['content']
            strategy = postForm.cleaned_data['strategy']
            author = request.user
            stock = stock
            post = Post(title = title, content = content, author = author, stock = stock, strategy = strategy)
            post.save()
            return redirect('stockInfo', stockCode)
    return render(request, 'post/newPost.html', {'postForm':postForm, 'stock':stock})        

# 폼 에러 제외 폼 활용
@cache_control(no_cache = True, must_revalidate = True)
def editPost(request, postPk):
    post = Post.objects.get(pk = postPk)
    if request.method == 'POST':
        titleTmp = request.POST.get('title')
        contentTmp = request.POST.get('content')
        strategyTmp = request.POST.get('strategy') 
        if titleTmp != '':
            post.title = titleTmp
        else:
            editTError = '제목이 비어있으면 안됨'
            return render(request, 'post/editPost.html',{'post':post, 'editTError':editTError})  
        if len(contentTmp)!= 0:
            post.content = contentTmp
        else:
            editCError = '내용이 비어있으면 안됨'
            return render(request, 'post/editPost.html',{'post':post, 'editCError':editCError})  
        post.strategy = strategyTmp
        post.updatedAt = timezone.now()
        post.save()
        return redirect('detailPost', post.pk)       
    return render(request, 'post/editPost.html',{'post':post})  
 
@cache_control(no_cache = True, must_revalidate = True)
def deletePost(request, postPk, stockCode):
    post = Post.objects.get(pk = postPk)
    post.delete()
    return redirect('stockInfo', stockCode)

@cache_control(no_cache = True, must_revalidate = True)
def likePost(request, postPk): 
    if request.method == 'POST':
        post = Post.objects.get(pk = postPk)
        if request.user in post.likeUsers.all():
            post.likeUsers.remove(request.user)
            post.likeCount -= 1 
        else:
            post.likeUsers.add(request.user)
            post.likeCount += 1
        post.save()
        return redirect('detailPost', postPk)
    else:
        raise Http404('글 작성 좋아요 메서드 에러')
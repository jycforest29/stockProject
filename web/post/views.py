from django.shortcuts import render, redirect
import yfinance as yf
from matplotlib import pyplot as plt
import pandas as pd
from .forms import PostForm
from comment.forms import CommentForm
from stock.models import Stock
from .models import Post
from comment.models import Comment
from django.http import Http404

# Create your views here.

def detailPost(request, postPk):
    post = Post.objects.get(pk = postPk)
    commentForm = CommentForm()
    userInPostLikes = False
    comments = Comment.objects.filter(post = post)
    if post.likeCount != 0:
        if request.user in post.likeUsers.all():
            userInPostLikes = True 
    return render(request, 'post/detailPost.html', {'post':post, 'userInPostLikes':userInPostLikes, 'commentForm':commentForm, 'comments':comments})

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
            #  Field 'id' expected a number but got <SimpleLazyObject: 
            post = Post(title = title, content = content, author = author, stock = stock, strategy = strategy)
            post.save()
            # post.save()는 필수? 
            return redirect('stockInfo', stockCode)
    # 하나는 html에 필요한 변수, 하나는 매개변수 - 매개변수여서라기 보다는 newPost.html에서 필요해서
    return render(request, 'post/newPost.html', {'postForm':postForm, 'stock':stock})        

def editPost(request, postPk):
    editForm = PostForm() 
    post = Post.objects.get(pk = postPk)
    if request.method == 'POST':
        editForm = PostForm(request.POST)
        if editForm.is_valid():
            post.title = editForm.cleaned_data['title']
            post.content = editForm.cleaned_data['content']
            post.strategy = editForm.cleaned_data['strategy']
            post.save()
            return redirect('detailPost', post.pk)
    # 하나는 html에 필요한 변수, 하나는 매개변수 - 적용안함?        
    return render(request, 'post/editPost.html', {'editForm':editForm, 'post':post})  
 
def deletePost(request, postPk, stockCode):
    post = Post.objects.get(pk = postPk)
    post.delete()
    return redirect('stockInfo', stockCode)

def reComment(request, commentPk, postPk):
    return redirect('detailPost', postPk)

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
        raise Http404('포스트 좋아요 메서드 에러')
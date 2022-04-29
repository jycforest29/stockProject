from django.http import Http404
from django.shortcuts import render, redirect
from .models import Comment
from post.models import Post
from .forms import CommentForm

# Create your views here.

def newComment(request, postPk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(pk = postPk) 
            content = form.cleaned_data['content'] 
            comment = Comment(post = post, author = request.user, content = content)
            post.commentCount += 1
            comment.save()
            post.save()
            return redirect('detailPost', postPk)
    else:
        raise Http404('코멘트 작성 메서드 에러') 

def editComment(request, commentPk, postPk): 
    editForm = CommentForm()
    post = Post.objects.get(pk = postPk)
    comments = Comment.objects.filter(post = post)
    if request.method == 'POST':
        editForm = CommentForm(request.POST)
        if editForm.is_valid():
            content = editForm.cleaned_data['content']
            comment = Comment.objects.get(pk = commentPk)
            comment.content = content
            comment.save() 
            return redirect('detailPost', postPk)
    return render(request, 'post/detailPost.html', {'post':post,'comments':comments, 'editForm':editForm})

def deleteComment(request, commentPk, postPk):
    comment = Comment.objects.get(pk = commentPk)
    comment.delete()
    post = Post.objects.get(pk = postPk)
    post.commentCount -= 1
    post.save()
    return redirect('detailPost', postPk)  

def likeComment(request, commentPk):
    if request.method == 'POST':
        comment = Comment.objects.get(pk = commentPk)
        if request.user in comment.likeUsers.all():
            comment.likeUsers.remove(request.user)
            comment.likeCount -= 1
        else:
            comment.likeUsers.add(request.user)
            comment.likeCount += 1
        comment.save()
        return redirect('detailPost', commentPk) 
    else:
        raise Http404('댓글 좋아요 메서드 에러')
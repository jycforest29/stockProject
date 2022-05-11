from django.http import Http404
from django.shortcuts import render, redirect
from .models import Comment, CommentBase
from post.models import Post
from .forms import CommentForm, EditForm, ReCommentForm
from django.utils import timezone
from django.views.decorators.cache import cache_control

# Create your views here.

# 폼 활용
@cache_control(no_cache = True, must_revalidate = True)
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

# 폼 활용하지 않음
@cache_control(no_cache = True, must_revalidate = True)
def editComment(request, commentPk, postPk): 
    editForm = EditForm()
    post = Post.objects.get(pk = postPk)
    comments = Comment.objects.filter(post = post)
    comment = Comment.objects.get(pk = commentPk)
    if request.method == 'POST':
        editForm = EditForm(request.POST)
        editCmtValue = request.POST.get('editCmtValue')
        if editCmtValue == '':
            cmtError = '댓글 내용이 있어야함'
            return render(request, 'post/detailPost.html', {'post':post,'comments':comments, 'editForm':editForm, 'commentPk': commentPk, 'cmtError':cmtError})
        comment.content = editCmtValue
        comment.updatedAt = timezone.now()
        comment.save() 
        return redirect('detailPost', postPk)
    return render(request, 'post/detailPost.html', {'post':post,'comments':comments, 'editForm':editForm, 'commentPk': commentPk})

@cache_control(no_cache = True, must_revalidate = True)
def deleteComment(request, commentPk, postPk):
    comment = Comment.objects.get(pk = commentPk)    
    post = Post.objects.get(pk = postPk)
    commentNum = comment.reComment.all().count() + 1
    post.commentCount -= commentNum
    post.save()
    comment.delete()
    return redirect('detailPost', postPk)  

@cache_control(no_cache = True, must_revalidate = True)
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
        return redirect('detailPost', comment.post.pk) 
    else:
        raise Http404('댓글 좋아요 메서드 에러')

# 폼 활용
@cache_control(no_cache = True, must_revalidate = True)
def newReComment(request, commentPk, postPk):
    if request.method == 'POST':
        form = ReCommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(pk = postPk) 
            post.commentCount += 1
            post.save()

            content = form.cleaned_data['content'] 
            reComment = CommentBase(author = request.user, content = content)            
            reComment.save()

            comment = Comment.objects.get(pk = commentPk) 
            comment.reComment.add(reComment)
            comment.save()
            return redirect('detailPost', postPk)
    else:
        raise Http404('리코멘트 작성 메서드 에러') 

# 폼 활용하지 않음
@cache_control(no_cache = True, must_revalidate = True)
def editReComment(request, reCommentPk, postPk): 
    editReForm = EditForm()
    post = Post.objects.get(pk = postPk)
    comments = Comment.objects.filter(post = post)
    reComment = CommentBase.objects.get(pk = reCommentPk)
    if request.method == 'POST':
        editReForm = EditForm(request.POST)
        editReCmtValue = request.POST.get('editReCmtValue')
        if editReCmtValue == '':
            cmtError = '댓글 내용이 있어야함'
            return render(request, 'post/detailPost.html', {'post':post,'comments':comments, 'editReForm':editReForm, 'reCommentPk': reCommentPk, 'cmtError':cmtError})
        reComment.content = editReCmtValue
        reComment.updatedAt = timezone.now()
        reComment.save() 
        return redirect('detailPost', postPk)
    return render(request, 'post/detailPost.html', {'post':post,'comments':comments, 'editReForm':editReForm, 'reCommentPk': reCommentPk})

@cache_control(no_cache = True, must_revalidate = True)
def deleteReComment(request, reCommentPk, postPk):
    reComment = CommentBase.objects.get(pk = reCommentPk)
    reComment.delete()

    post = Post.objects.get(pk = postPk)
    post.commentCount -= 1
    post.save()
    return redirect('detailPost', postPk)  

@cache_control(no_cache = True, must_revalidate = True)
def likeReComment(request, reCommentPk, postPk):
    if request.method == 'POST':
        reComment = CommentBase.objects.get(pk = reCommentPk)
        if request.user in reComment.likeUsers.all():
            reComment.likeUsers.remove(request.user)
            reComment.likeCount -= 1
        else:
            reComment.likeUsers.add(request.user)
            reComment.likeCount += 1
        reComment.save()
        return redirect('detailPost', postPk) 
    else:
        raise Http404('댓글 좋아요 메서드 에러')

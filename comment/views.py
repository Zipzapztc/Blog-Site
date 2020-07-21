from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm

def update_comment(request):
    comment_form=CommentForm(request.POST,user=request.user)
    data={}
    if comment_form.is_valid():
        comment=Comment()
        comment.content_object=comment_form.cleaned_data['content_object']
        comment.text=comment_form.cleaned_data['text']
        comment.user=comment_form.cleaned_data['user']

        #判断评论和回复
        parent=comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root=parent.root if parent.root is not None else parent
            comment.parent=parent
            comment.reply_to_user=parent.user
        comment.save()
        
        #发送邮件
        comment.send_email()

        data['status']='SUCCESS'
        data['text']=comment.text
        data['username']=comment.user.profile.nickname
        data['comment_time']=comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        if parent is not None:
            data['reply_to_user']=comment.reply_to_user.profile.nickname
        else:
            data['reply_to_user']=''
        data['id']=comment.id
        data['root_id']=comment.root.id if comment.root is not None else ''
        data['content_type']=ContentType.objects.get_for_model(comment).model
    else:
        data['status']='FAIL'
        data['message']=list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
    

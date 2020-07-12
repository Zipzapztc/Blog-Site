from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .models import Comment

def update_comment(request):
    referer=request.META.get('HTTP_REFERER',reverse('home'))

    try:
        content_type=request.POST.get('content_type','')
        object_id=int(request.POST.get('object_id',''))
        model_type=ContentType.objects.get(model=content_type).model_class()
        model_object=model_type.objects.get(id=object_id)
    except Exception:
        return render(request,'error.html',{ 'message':'评论对象不存在','redirect_address':referer })
    
    text=request.POST.get('text','').strip()
    if text=='':
        return render(request,'error.html',{ 'message':'评论内容为空','redirect_address':referer })
    user=request.user
    if not user.is_authenticated:
        return render(request,'error.html',{ 'message':'用户未登录','redirect_address':referer })

    comment=Comment()
    comment.content_object=model_object
    comment.text=text
    comment.user=user
    comment.save()

    return redirect(referer)
    

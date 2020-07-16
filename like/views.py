from django.shortcuts import render
from django.http import JsonResponse
from django.db.models.fields import exceptions
from django.contrib.contenttypes.models import ContentType
from .models import LikeCount,LikeRecord

def FailResponse(message):
    data={}
    data['status']='FAIL'
    data['message']=message
    return JsonResponse(data)

def SuccessResponse(like_num):
    data={}
    data['status']='SUCCESS'
    data['like_num']=like_num
    return JsonResponse(data)

def like_change(request):
    user=request.user
    if not user.is_authenticated:
        return FailResponse('用户未登录')

    content_type=request.GET.get('content_type')
    object_id=int(request.GET.get('object_id'))
    try:
        content_type=ContentType.objects.get(model=content_type)
        model_class=content_type.model_class()
        model_object=model_class.objects.get(id=object_id)
    except exceptions.ObjectDoesNotExist:
        return FailResponse('对象不存在')

    is_like=request.GET.get('is_like')
    if is_like=='true':
        #点赞
        like_record,created=LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)
        if created:
            like_count,created=LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            like_count.like_num +=1
            like_count.save()
            return SuccessResponse(like_count.like_num)
        else:
            return FailResponse('你已经点赞过了')
    else:
        #取消点赞
        if LikeRecord.objects.filter(content_type=content_type,object_id=object_id,user=user).exists():
            like_record=LikeRecord.objects.get(content_type=content_type,object_id=object_id,user=user)
            like_record.delete()
            
            like_count,created=LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            if not created:
                like_count.like_num-=1
                like_count.save()
                return SuccessResponse(like_count.like_num)
            else:
                return FailResponse('数据错误')
        else:
            return FailResponse('你没有点赞过')



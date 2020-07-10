from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from read_statistic.utils import get_week_read_num
from blog.models import Blog

def home(request):
    content_type=ContentType.objects.get_for_model(Blog)
    dates,read_num=get_week_read_num(content_type)
    context={}
    context['dates']=dates
    context['read_nums']=read_num
    return render(request,'home.html',context)
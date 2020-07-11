from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from read_statistic.utils import get_week_read_num
from blog.models import Blog
from blog.utils import get_week_hot_blog,get_month_hot_blog
from read_statistic.utils import get_today_hot_blog,get_yesterday_hot_blog


def home(request):
    content_type=ContentType.objects.get_for_model(Blog)
    dates,read_num=get_week_read_num(content_type)
    today_hot_blog=get_today_hot_blog(content_type)
    yesterday_hot_blog=get_yesterday_hot_blog(content_type)

    #缓存本周热门文章
    week_hot_blog=cache.get('week_hot_blog')
    if not week_hot_blog:
        week_hot_blog=get_week_hot_blog()
        cache.set('week_hot_blog',week_hot_blog,3600)
    
    #缓存本月热门文章
    month_hot_blog=cache.get('month_hot_blog')
    if not month_hot_blog:
        month_hot_blog=get_month_hot_blog()
        cache.set('month_hot_blog',month_hot_blog,3600)

    context={}
    context['dates']=dates
    context['read_nums']=read_num
    context['today_hot_blog']=today_hot_blog
    context['yesterday_hot_blog']=yesterday_hot_blog
    context['week_hot_blog']=week_hot_blog
    context['month_hot_blog']=month_hot_blog
    return render(request,'home.html',context)


def log_in(request):
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return render(request,'error.html',{ 'message':'用户名或密码错误'})
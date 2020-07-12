from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.core.cache import cache
from read_statistic.utils import get_week_read_num
from blog.models import Blog
from blog.utils import get_week_hot_blog,get_month_hot_blog
from read_statistic.utils import get_today_hot_blog,get_yesterday_hot_blog
from django.urls import reverse
from .forms import LoginForm,RegisterForm

def home(request):
    content_type=ContentType.objects.get_for_model(Blog)
    dates,read_num=get_week_read_num(content_type)
    today_hot_blog=get_today_hot_blog(content_type)
    yesterday_hot_blog=get_yesterday_hot_blog(content_type)

    #缓存本周热门文章
    week_hot_blog=cache.get('week_hot_blog')
    if week_hot_blog is None:
        week_hot_blog=get_week_hot_blog()
        cache.set('week_hot_blog',week_hot_blog,3600)
    
    #缓存本月热门文章
    month_hot_blog=cache.get('month_hot_blog')
    if month_hot_blog is None:
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
    if request.method=='POST':
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user=login_form.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form=LoginForm()
    context={}
    context['login_form']=login_form
    return render(request,'login.html',context)

def register(request):
    if request.method=='POST':
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            username=register_form.cleaned_data['username']
            email=register_form.cleaned_data['email']
            password=register_form.cleaned_data['password']
            new_user=User.objects.create_user(username,email,password)
            new_user.save()

            user=authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        register_form=RegisterForm()
    context={}
    context['register_form']=register_form
    return render(request,'register.html',context)
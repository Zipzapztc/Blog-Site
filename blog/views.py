from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from .models import BlogType,Blog
from read_statistic.utils import read_num_add_one
from comment.models import Comment

def blog_list_common(request,blog_all):
    paginator=Paginator(blog_all,settings.EACH_PAGE_BLOG_NUM)
    current_page_num=request.GET.get('page',1)
    blogs=paginator.get_page(int(current_page_num))

    page_range=[page_num for page_num in range(int(current_page_num)-2,int(current_page_num)+3) if 0 <page_num<= paginator.num_pages]
    if page_range[0]-1 > 1:
        page_range.insert(0,'...')
    if page_range[-1]+1 < paginator.num_pages:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context={}
    context['blogs']=blogs
    context['page_range']=page_range
    context['blog_types']=BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates']=Blog.objects.dates('create_time','month',order='DESC')
    return context

def blog_list(request):
    blog_all=Blog.objects.all()
    context=blog_list_common(request,blog_all)
    return render(request,'blog_list.html',context)


def blog_with_type(request,blog_type_id):
    blog_type=get_object_or_404(BlogType,id=blog_type_id)
    blog_all=Blog.objects.filter(blog_type=blog_type)

    context=blog_list_common(request,blog_all)
    context['blog_type']=blog_type
    return render(request,'blog_with_type.html',context)


def blog_with_date(request,year,month):
    blog_all=Blog.objects.filter(create_time__year=year,create_time__month=month)

    context=blog_list_common(request,blog_all)
    context['blog_date']='%d年%d月'%(year,month)
    return render(request,'blog_with_date.html',context)

def blog_detail(request,blog_id):
    blog=get_object_or_404(Blog,id=blog_id)
    cookie_name=read_num_add_one(request,blog)
    content_type=ContentType.objects.get_for_model(blog)
    comments=Comment.objects.filter(content_type=content_type,object_id=blog.id)

    context={}
    context['previous_blog']=Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['blog']=blog
    context['next_blog']=Blog.objects.filter(create_time__lt=blog.create_time).first()
    context['comments']=comments
    response=render(request,'blog_detail.html',context)
    response.set_cookie(cookie_name,'true')
    return response
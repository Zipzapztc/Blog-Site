from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.cache import cache
from read_statistic.utils import get_week_read_num
from blog.models import Blog
from blog.views import blog_list_common
from blog.utils import get_week_hot_blog,get_month_hot_blog
from read_statistic.utils import get_today_hot_blog,get_yesterday_hot_blog


def home(request):
    content_type = ContentType.objects.get_for_model(Blog)
    dates,read_num = get_week_read_num(content_type)
    today_hot_blog = get_today_hot_blog(content_type)
    yesterday_hot_blog = get_yesterday_hot_blog(content_type)

    #缓存本周热门文章
    week_hot_blog = cache.get('week_hot_blog')
    if week_hot_blog is None:
        week_hot_blog = get_week_hot_blog()
        cache.set('week_hot_blog', week_hot_blog, 3600)
    
    #缓存本月热门文章
    month_hot_blog = cache.get('month_hot_blog')
    if month_hot_blog is None:
        month_hot_blog = get_month_hot_blog()
        cache.set('month_hot_blog', month_hot_blog, 3600)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_num
    context['today_hot_blog'] = today_hot_blog
    context['yesterday_hot_blog'] = yesterday_hot_blog
    context['week_hot_blog'] = week_hot_blog
    context['month_hot_blog'] = month_hot_blog
    return render(request, 'home.html', context)


def search(request):
    search_word = request.GET.get('search_word','').strip()
    condition = None
    for word in search_word.split(' '):
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = condition | Q(title__icontains=word)

    if condition is not None:        
        search_blogs = Blog.objects.filter(condition)
    else:
        search_blogs = Blog.objects.all()

    context = blog_list_common(request,search_blogs)
    context['search_word'] = search_word
    context['search_blogs_count'] = search_blogs.count()
    return render(request, 'search.html', context)

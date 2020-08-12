import datetime
from django.utils import timezone
from django.db.models import Sum,Max
from .models import Blog


def get_week_hot_blog():
    today = timezone.localtime().date()
    week_ago = today-datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_detail__date__lte=today, read_detail__date__gt=week_ago) \
                    .values('id','title').annotate(read_num_sum=Sum('read_detail__read_num')).order_by('-read_num_sum')
    return blogs[:5]


def get_month_hot_blog():
    today = timezone.localtime().date()
    month_ago = today-datetime.timedelta(days=30)
    blogs = Blog.objects.filter(read_detail__date__lte=today, read_detail__date__gt=month_ago) \
                    .values('id','title').annotate(read_num_sum=Sum('read_detail__read_num')).order_by('-read_num_sum')
    return blogs[:5]
    
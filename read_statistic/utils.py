import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from .models import ReadNum,ReadDetail
from django.utils import timezone


def read_num_add_one(request,obj):
    content_type = ContentType.objects.get_for_model(obj)
    cookie_name = '%s_%d_read' % (content_type, obj.id)
    if not request.COOKIES.get(cookie_name):
        readnum, created = ReadNum.objects.get_or_create(content_type=content_type, object_id=obj.id)
        readnum.read_num += 1
        readnum.save()

        readdetail, created = ReadDetail.objects.get_or_create(content_type=content_type, object_id=obj.id, date=timezone.localtime().date())
        readdetail.read_num += 1
        readdetail.save()
    return cookie_name


def get_week_read_num(content_type):
    today = timezone.localtime().date()
    dates = []
    read_nums = []
    for i in range(6,-1,-1):
        date = today-datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_detail = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_detail.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


def get_today_hot_blog(content_type):
    today = timezone.localtime().date()
    blogs = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return blogs[:5]


def get_yesterday_hot_blog(content_type):
    today = timezone.localtime().date()
    yesterday = today-datetime.timedelta(days=1)
    blogs = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return blogs[:5]

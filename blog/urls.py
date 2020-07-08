from django.urls import path
from .views import blog_detail,blog_list,blog_with_type,blog_with_date

#http://localhost:8000/blog
urlpatterns = [
    path('',blog_list,name='blog_list'),
    path('<int:blog_id>',blog_detail,name='blog_detail'),
    path('type/<int:blog_type_id>',blog_with_type,name='blog_with_type'),
    path('date/<int:year>/<int:month>',blog_with_date,name='blog_with_date'),
]
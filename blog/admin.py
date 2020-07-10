from django.contrib import admin
from .models import BlogType,Blog

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display=('id','type_name')
    ordering=('-id',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=('id','title','blog_type','author','get_read_num','create_time','last_update_time')
    ordering=('-id',)
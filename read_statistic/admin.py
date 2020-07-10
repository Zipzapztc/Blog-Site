from django.contrib import admin
from .models import ReadNum,ReadDetail

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display=['content_object','read_num']

@admin.register(ReadDetail)
class ReadNumDetailAdmin(admin.ModelAdmin):
    list_display=['content_object','date','read_num']
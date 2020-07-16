from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistic.models import ReadNumExpand,ReadDetail

class BlogType(models.Model):
    type_name=models.CharField(max_length=20)

    def __str__(self):
        return self.type_name
    

class Blog(models.Model,ReadNumExpand):
    title=models.CharField(max_length=50)
    blog_type=models.ForeignKey(BlogType,on_delete=models.CASCADE)
    content=RichTextUploadingField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    read_detail=GenericRelation(ReadDetail)
    create_time=models.DateTimeField(auto_now_add=True)
    last_update_time=models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return '<Blog:%s>' % self.title
    
    class Meta:
        ordering=['-create_time']

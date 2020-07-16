from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text=models.TextField() 
    user=models.ForeignKey(User,related_name='comment_user',on_delete=models.CASCADE)
    comment_time=models.DateTimeField(auto_now_add=True)

    root=models.ForeignKey('self',related_name='leaf_comment',null=True,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',related_name='child_comment',null=True,on_delete=models.CASCADE)
    reply_to_user=models.ForeignKey(User,related_name='reply_user',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering=['comment_time']
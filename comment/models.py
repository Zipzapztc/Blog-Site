from threading import Thread
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail


class SendEmail(Thread):
    def __init__(self,subject,text,email,fail_silently=False):
        super().__init__()
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently

    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently = self.fail_silently,
            html_message = self.text
        )

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField() 
    user = models.ForeignKey(User, related_name = 'comment_user', on_delete = models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add = True)

    root = models.ForeignKey('self', related_name = 'leaf_comment', null = True, on_delete = models.CASCADE)
    parent = models.ForeignKey('self', related_name = 'child_comment', null = True, on_delete = models.CASCADE)
    reply_to_user = models.ForeignKey(User, related_name = 'reply_user', null = True, on_delete = models.CASCADE)

    def send_email(self):
        if self.parent == None:
            #评论博客
            subject = '有人评论你的博客'
            email = self.content_object.author.email
        else:
            #回复评论
            subject = '有人回复你的评论'
            email = self.reply_to_user.email
        if email != '':
            context = {}
            context['comment_text'] = self.text
            context['url'] = reverse('blog_detail', kwargs = {'blog_id': self.content_object.id})
            text = render_to_string('send_email.html', context)
            send_email = SendEmail(subject, text, email)
            send_email.start()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
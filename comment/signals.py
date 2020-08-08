from threading import Thread
from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import Comment


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    if instance.parent == None:
        recipient = instance.content_object.author
        verb = '%s评论了你的文章《%s》' % (instance.user.profile.nickname, instance.content_object.title)
    else:
        recipient = instance.reply_to_user
        verb = '%s回复了你的评论“%s”' % (instance.user.profile.nickname, strip_tags(instance.parent.text))
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance)


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


@receiver(post_save, sender=Comment)
def send_email(sender, instance, **kwargs):
    if instance.parent is None:
        #评论博客
        subject = '有人评论了你的文章'
        email = instance.content_object.author.email
    else:
        #回复评论
        subject = '有人回复了你的评论'
        email = instance.reply_to_user.email
    if email != '':
        context = {}
        context['comment_text'] = instance.text
        context['url'] = reverse('blog_detail', kwargs = {'blog_id': instance.content_object.id})
        text = render_to_string('send_email.html', context)
        send_email = SendEmail(subject, text, email)
        send_email.start()
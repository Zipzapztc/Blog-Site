from django.db.models.signals import post_save
from notifications.signals import notify
from django.utils.html import strip_tags
from django.dispatch import receiver
from .models import LikeRecord


@receiver(post_save, sender=LikeRecord)
def send_notification(sender, instance, **kwargs):
    if instance.content_type.model == 'blog':
        recipient = instance.content_object.author
        verb = '%s点赞了你的文章《%s》' % (instance.user.profile.nickname, instance.content_object.title)
    else:
        recipient = instance.content_object.user
        verb = '%s点赞了你的评论“%s”' % (instance.user.profile.nickname, strip_tags(instance.content_object.text))
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance)
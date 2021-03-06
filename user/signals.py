from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def send_notification(sender, instance, **kwargs):
    if kwargs['created'] == True:
        verb = '注册成功,欢迎来到“云游闲人”'
        url = reverse('user_info')
        notify.send(instance, recipient=instance, verb=verb, action_object=instance, url=url)
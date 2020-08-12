from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, verbose_name='昵称')

    def __str__(self):
        return '<profile：%s for %s>' % (self.nickname, self.user.username)


class OAuthRelationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    openid = models.CharField(max_length=128)

    OAUTH_TYPE_CHOICES = (
        (0, "QQ"),
        (1, "WeChat"),
        (2, "Github"),
    )
    oauth_type = models.IntegerField(default=0, choices=OAUTH_TYPE_CHOICES)

    def __str__(self):
        return '<OAuthRelationship：%s>' % self.user
    
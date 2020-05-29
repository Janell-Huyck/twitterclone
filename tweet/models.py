from django.db import models
from twitteruser.models import TwitterUser
from django.utils import timezone


class Tweet(models.Model):
    author = models.ForeignKey(TwitterUser, on_delete=models.CASCADE,)
    text = models.CharField(max_length=140)
    tweet_time = models.DateTimeField(default=timezone.now)

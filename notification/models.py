from django.db import models
from twitteruser.models import TwitterUser
from tweet.models import Tweet


class Notification(models.Model):
    victim = models.ForeignKey(
        TwitterUser, related_name="victim", on_delete=models.CASCADE
    )
    tweet_id = models.ForeignKey(
        Tweet, related_name="tweet_id", on_delete=models.CASCADE
    )
    viewed = models.BooleanField(default=False)

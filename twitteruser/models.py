from django.db import models
from django.contrib.auth.models import AbstractUser


class TwitterUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50)
    following = models.ManyToManyField("self", symmetrical=False, blank=True)

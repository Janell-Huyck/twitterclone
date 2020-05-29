from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.urls import reverse


class TwitterUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50)
    following = models.ManyToManyField("self", symmetrical=False, blank=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    REQUIRED_FIELDS = [
        "slug",
        "display_name",
    ]

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

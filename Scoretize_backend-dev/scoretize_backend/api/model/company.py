from django.db import models
from django.utils import timezone


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255, blank=False)
    join_date = models.DateTimeField(default=timezone.now)
    facebook_url = models.CharField(max_length=255, blank=False, null=True)
    instagram_url = models.CharField(max_length=255, blank=False, null=True)
    twitter_url = models.CharField(max_length=255, blank=False, null=True)
    youtube_url = models.CharField(max_length=255, blank=False, null=True)

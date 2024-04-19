from django.db import models
from django.utils import timezone


class Social_links(models.Model):
    project = models.OneToOneField(
        'Project', on_delete=models.CASCADE, unique=True, primary_key=True)
    modified_date = models.DateTimeField(default=timezone.now)
    facebook_url = models.CharField(max_length=255, blank=False, null=True)
    instagram_url = models.CharField(max_length=255, blank=False, null=True)
    twitter_url = models.CharField(max_length=255, blank=False, null=True)
    youtube_url = models.CharField(max_length=255, blank=False, null=True)
    company_id = models.BigIntegerField(blank=False)

from django.db import models


class Facebook(models.Model):
    id = models.AutoField(primary_key=True)
    social_media = models.ForeignKey(
        'Social_media', on_delete=models.SET_NULL, null=True)
    likes = models.BigIntegerField(blank=False, null=True)
    followers = models.BigIntegerField(blank=False, null=True)
    avg_post_likes = models.FloatField(max_length=255, blank=False, null=True)
    avg_post_comments = models.FloatField(
        max_length=255, blank=False, null=True)
    avg_post_shares = models.FloatField(max_length=255, blank=False, null=True)
    fb_engagement_rate = models.FloatField(blank=False, null=True)

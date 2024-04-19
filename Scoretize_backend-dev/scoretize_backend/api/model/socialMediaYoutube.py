from django.db import models


class Youtube(models.Model):
    id = models.AutoField(primary_key=True)
    social_media = models.ForeignKey(
        'Social_media', on_delete=models.SET_NULL, null=True)
    video_count = models.BigIntegerField(blank=False, null=True)
    view_count = models.BigIntegerField(blank=False, null=True)
    subscriber_count = models.BigIntegerField(blank=False, null=True)
    like_count = models.BigIntegerField(blank=False, null=True)
    comment_count = models.BigIntegerField(blank=False, null=True)
    youtube_engagement_rate = models.FloatField(blank=False, null=True)

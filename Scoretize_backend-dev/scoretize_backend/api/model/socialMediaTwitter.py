from django.db import models


class Twitter(models.Model):
    id = models.AutoField(primary_key=True)
    social_media = models.ForeignKey(
        'Social_media', on_delete=models.SET_NULL, null=True)
    followers_count = models.BigIntegerField(blank=False, null=True)
    following_count = models.BigIntegerField(blank=False, null=True)
    avg_retweet_count = models.FloatField(
        max_length=255, blank=False, null=True)
    avg_reply_count = models.FloatField(max_length=255, blank=False, null=True)
    avg_likes_count = models.FloatField(max_length=255, blank=False, null=True)
    listed_count = models.BigIntegerField(blank=False, null=True)
    tweet_count = models.BigIntegerField(blank=False, null=True)
    twitter_engagement_rate = models.FloatField(blank=False, null=True)

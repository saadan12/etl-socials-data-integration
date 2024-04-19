from django.db import models


class Industry_wise_scores(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        'Project', on_delete=models.SET_NULL, null=True)
    initial_date = models.DateTimeField(auto_now=True)
    company_id = models.BigIntegerField(blank=False)
    global_score = models.FloatField(max_length=255, blank=False)
    website_score = models.FloatField(max_length=255, blank=False)
    sm_score = models.FloatField(max_length=255, blank=False)
    sm_facebook_score = models.FloatField(max_length=255, blank=False)
    sm_instagram_score = models.FloatField(max_length=255, blank=False)
    sm_youtube_score = models.FloatField(max_length=255, blank=False)
    sm_twitter_score = models.FloatField(max_length=255, blank=False)
    seo_score = models.FloatField(max_length=255, blank=False)

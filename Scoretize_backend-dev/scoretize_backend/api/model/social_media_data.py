from django.db import models


class Social_media(models.Model):
    social_id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(
        'Company', on_delete=models.SET_NULL, null=True)
    initial_date = models.DateTimeField(auto_now=True)
    global_engagement_rate = models.FloatField(
        max_length=255, blank=False, null=True)
    total_followers = models.BigIntegerField(blank=False, null=True)
    total_average_interactions = models.FloatField(
        max_length=255, blank=False, null=True)
    total_clicks = models.BigIntegerField(blank=False, null=True)
    project_id = models.BigIntegerField(blank=False, null=False, default=0)
    data_date = models.DateTimeField(auto_now=True)

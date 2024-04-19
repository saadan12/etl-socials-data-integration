from django.db import models


class Website(models.Model):
    website_id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(
        'Company', on_delete=models.SET_NULL, null=True)
    initial_date = models.DateTimeField(auto_now=True)
    mobile_page_speed = models.FloatField(
        max_length=255, blank=False, null=True)
    desktop_page_speed = models.FloatField(
        max_length=255, blank=False, null=True)
    bounce_rate = models.FloatField(max_length=255, blank=False, null=True)
    monthly_traffic = models.FloatField(max_length=255, blank=False, null=True)
    pages_visit = models.FloatField(max_length=255, blank=False, null=True)
    avg_TimeOnSite = models.CharField(max_length=255, blank=False, null=True)
    data_date = models.DateTimeField(auto_now=True)

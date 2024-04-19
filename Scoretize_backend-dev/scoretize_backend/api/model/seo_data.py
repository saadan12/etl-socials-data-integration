from django.db import models


class Seo(models.Model):
    seo_id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(
        'Company', on_delete=models.SET_NULL, null=True)
    initial_date = models.DateTimeField(auto_now=True)
    organic_traffic = models.FloatField(max_length=255, blank=False, null=True)
    web_authority = models.FloatField(max_length=255, blank=False, null=True)
    total_keywords = models.FloatField(max_length=255, blank=False, null=True)
    avg_keywords_search = models.FloatField(
        max_length=255, blank=False, null=True)
    traffic_value = models.FloatField(max_length=255, blank=False, null=True)
    paid_traffic = models.FloatField(max_length=255, blank=False, null=True)
    estimatedCPC = models.FloatField(max_length=255, blank=False, null=True)
    paid_keywords = models.FloatField(max_length=255, blank=False, null=True)
    estm_ppc_budget = models.FloatField(max_length=255, blank=False, null=True)
    backlinks = models.FloatField(max_length=255, blank=False, null=True)
    referring_domains = models.FloatField(
        max_length=255, blank=False, null=True)
    avg_organic_rank = models.FloatField(
        max_length=255, blank=False, null=True)
    data_date = models.DateTimeField(auto_now=True)

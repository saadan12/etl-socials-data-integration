from django.db import models
from django.utils import timezone


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(
        'Company', on_delete=models.SET_NULL, null=True)
    sector = models.ForeignKey('Sector', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, blank=False, default='name')
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BigIntegerField(default=True)
    competitor_1 = models.CharField(max_length=255, blank=False)
    competitor_2 = models.CharField(max_length=255, blank=False)
    competitor_3 = models.CharField(max_length=255, blank=False, null=True)
    competitor_4 = models.CharField(max_length=255, blank=False, null=True)
    competitor_5 = models.CharField(max_length=255, blank=False, null=True)
    competitor_6 = models.CharField(max_length=255, blank=False, null=True)
    competitor_7 = models.CharField(max_length=255, blank=False, null=True)
    competitor_8 = models.CharField(max_length=255, blank=False, null=True)
    competitor_9 = models.CharField(max_length=255, blank=False, null=True)
    competitor_10 = models.CharField(max_length=255, blank=False, null=True)

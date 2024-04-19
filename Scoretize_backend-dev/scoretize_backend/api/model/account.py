from django.db import models


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    public_id = models.BigIntegerField(blank=True)
    name = models.CharField(max_length=255, blank=False)
    adress = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    vat = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

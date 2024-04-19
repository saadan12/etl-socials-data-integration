from django.db import models


class Website_traffic(models.Model):
    id = models.AutoField(primary_key=True)
    website = models.ForeignKey(
        'Website', on_delete=models.SET_NULL, null=True)
    direct_traffic = models.BigIntegerField(blank=False, null=True)
    paid_traffic = models.BigIntegerField(blank=False, null=True)
    organic_traffic = models.BigIntegerField(blank=False, null=True)
    country_first = models.CharField(max_length=255, blank=False, null=True)
    country_second = models.CharField(max_length=255, blank=False, null=True)
    country_third = models.CharField(max_length=255, blank=False, null=True)
    country_forth = models.CharField(max_length=255, blank=False, null=True)
    country_fifth = models.CharField(max_length=255, blank=False, null=True)
    country_value_first = models.BigIntegerField(
        blank=False, null=True)
    country_value_second = models.BigIntegerField(
        blank=False, null=True)
    country_value_third = models.BigIntegerField(
        blank=False, null=True)
    country_value_forth = models.BigIntegerField(
        blank=False, null=True)
    country_value_fifth = models.BigIntegerField(
        blank=False, null=True)
    social_traffic = models.BigIntegerField(blank=False, null=True)
    social_first = models.CharField(max_length=255, blank=False, null=True)
    social_second = models.CharField(max_length=255, blank=False, null=True)
    social_third = models.CharField(max_length=255, blank=False, null=True)
    social_value_first = models.BigIntegerField(
        blank=False, null=True)
    social_value_second = models.BigIntegerField(
        blank=False, null=True)
    social_value_third = models.BigIntegerField(
        blank=False, null=True)
    reffered_traffic = models.BigIntegerField(blank=False, null=True)
    mail_traffic = models.BigIntegerField(blank=False, null=True)

from django.db import models


class Sector(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255, blank=False)
    subcategory = models.CharField(max_length=255, blank=False)

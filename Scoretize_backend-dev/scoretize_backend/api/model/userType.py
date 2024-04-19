from django.db import models


class User_Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, unique=True)
    description = models.CharField(max_length=255, blank=False)

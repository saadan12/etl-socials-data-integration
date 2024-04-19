from django.db import models
from django.utils import timezone


class PitchInputs(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.OneToOneField('Project', on_delete=models.CASCADE, unique=True)
    agency_name = models.CharField(max_length=255, blank=False, null=False)
    agency_domain = models.CharField(max_length=255, blank=False, null=False)
    brief = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.BigIntegerField(default=False)
    template = models.BigIntegerField(default=True)
from django.db import models


class UserProject(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(
        'Project', on_delete=models.SET_NULL, null=True)

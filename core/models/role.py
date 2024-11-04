from django.db import models

from core.models.permission import Permission


class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField('core.Permission')

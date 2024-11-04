from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=100)
    module = models.ForeignKey('core.Module', on_delete=models.PROTECT)